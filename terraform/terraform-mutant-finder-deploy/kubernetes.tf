variable "FLASK_APP" {
    type        = string
    description = "The name of the application."
}
variable "JWT_SECRET" {
    type        = string
    description = "JWT secret to encode the token."
}
variable "JWT_TOKEN_EXPIRES_IN_SECONDS" {
    type        = string
    description = "JWT token expiration time in seconds."
}
variable "MAGNETO_PASSWORD" {
    type        = string
    description = "Magneto's password to log into the application."
}
variable "DATABASE_HOST" {
    type        = string
    description = "Database host."
}
variable "DATABASE_PORT" {
    type        = string
    description = "Database port."
}
variable "DATABASE_NAME" {
    type        = string
    description = "Database name."
}
variable "DATABASE_USER" {
    type        = string
    description = "Database user."
}
variable "DATABASE_PASSWORD" {
    type        = string
    description = "Database password."
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.20.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }
  }
}

data "terraform_remote_state" "eks" {
  backend = "local"

  config = {
    path = "../terraform-mutant-finder-eks-cluster/terraform.tfstate"
  }
}

# Retrieve EKS cluster information
provider "aws" {
  region = data.terraform_remote_state.eks.outputs.region
}

data "aws_eks_cluster" "cluster" {
  name = data.terraform_remote_state.eks.outputs.cluster_id
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  exec {
    api_version = "client.authentication.k8s.io/v1alpha1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      data.aws_eks_cluster.cluster.name
    ]
  }
}

resource "kubernetes_deployment" "mutant_finder" {
  metadata {
    name = "scalable-mutant-finder"
    namespace = "prod-namespace"
    labels = {
      App = "ScalableMutantFinder"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        App = "ScalableMutantFinder"
      }
    }
    template {
      metadata {
        labels = {
          App = "ScalableMutantFinder"
        }
      }
      spec {
        container {
          image = "473200936731.dkr.ecr.us-east-2.amazonaws.com/mutant_finder:v1.0.0"
          image_pull_policy = "Always"
          name  = "mutant-finder"

          env {
            name = "FLASK_APP"
            value = "${var.FLASK_APP}"
          }

          env {
            name = "JWT_SECRET"
            value = "${var.JWT_SECRET}"
          }

          env {
            name = "JWT_TOKEN_EXPIRES_IN_SECONDS"
            value = "${var.JWT_TOKEN_EXPIRES_IN_SECONDS}"
          }

          env {
            name = "MAGNETO_PASSWORD"
            value = "${var.MAGNETO_PASSWORD}"
          }

          env {
            name = "DATABASE_HOST"
            value = "${var.DATABASE_HOST}"
          }

          env {
            name = "DATABASE_PORT"
            value = "${var.DATABASE_PORT}"
          }

          env {
            name = "DATABASE_NAME"
            value = "${var.DATABASE_NAME}"
          }

          env {
            name = "DATABASE_USER"
            value = "${var.DATABASE_USER}"
          }

          env {
            name = "DATABASE_PASSWORD"
            value = "${var.DATABASE_PASSWORD}"
          }

          port {
            container_port = 5000
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "100m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "mutant_finder" {
  metadata {
    name = "mutant-finder"
    namespace = "prod-namespace"
  }
  spec {
    selector = {
      App = kubernetes_deployment.mutant_finder.spec.0.template.0.metadata[0].labels.App
    }
    port {
      port        = 80
      target_port = 5000
    }

    type = "LoadBalancer"
  }
}

output "lb_ip" {
  value = kubernetes_service.mutant_finder.status.0.load_balancer.0.ingress.0.hostname
}

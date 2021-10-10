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

resource "kubernetes_deployment" "mutant_finder_database" {
  metadata {
    name = "mutant-finder-database"
    namespace = "prod-namespace"
    labels = {
      App = "MutantFinderDatabase"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        App = "MutantFinderDatabase"
      }
    }
    template {
      metadata {
        labels = {
          App = "MutantFinderDatabase"
        }
      }
      spec {
        container {
          image = "postgres:latest"
          name  = "database"

          env {
            name = "POSTGRES_DB"
            value = "${var.DATABASE_NAME}"
          }

          env {
            name = "POSTGRES_USER"
            value = "${var.DATABASE_USER}"
          }

          env {
            name = "POSTGRES_PASSWORD"
            value = "${var.DATABASE_PASSWORD}"
          }

          port {
            container_port = 5432
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "mutant_finder_database" {
  metadata {
    name = "mutant-finder-database"
    namespace = "prod-namespace"
  }
  spec {
    selector = {
      App = kubernetes_deployment.mutant_finder_database.spec.0.template.0.metadata[0].labels.App
    }
    port {
      port        = 5432
      target_port = 5432
    }

    type = "LoadBalancer"
  }
}

output "lb_ip" {
  value = kubernetes_service.mutant_finder_database.status.0.load_balancer.0.ingress.0.hostname
}

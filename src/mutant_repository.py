import psycopg2
import utils.database_utils

def save_human_dna_and_update_human_dna_statistics(dna_sequence_size, dna_sequence, is_mutant):

    def update_human_dna_statistics(is_mutant, cursor):
        if is_mutant:
            cursor.execute(
                " UPDATE human_dna_statistics SET " +
                "    count_mutant_dna = count_mutant_dna + 1, " +
                "    count_human_dna = count_human_dna + 1, " +
                "    ratio = CAST(CAST(count_mutant_dna + 1 AS DECIMAL) / CAST((count_human_dna + 1) AS DECIMAL) AS DECIMAL(5,4)); "
            )
        else:
            cursor.execute(
                " UPDATE human_dna_statistics SET " +
                "    count_human_dna = count_human_dna + 1, " +
                "    ratio = CAST(CAST(count_mutant_dna AS DECIMAL) / CAST((count_human_dna + 1) AS DECIMAL) AS DECIMAL(5,4)); "
            )

    connection = None
    dna_sequence_id = None
    try:
        connection = utils.database_utils.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO human_dna
                VALUES(gen_random_uuid(), %s, %s, %s)
                RETURNING id;
            """, (dna_sequence_size, dna_sequence, is_mutant))
        dna_sequence_id = cursor.fetchone()[0]
        update_human_dna_statistics(is_mutant, cursor)
        connection.commit()
        print('DNA sequence saved')
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
            return dna_sequence_id

def get_human_dna(dna_sequence):
    connection = None
    human_dna = None
    try:
        connection = utils.database_utils.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('SELECT is_mutant FROM human_dna WHERE dna_sequence = %s', dna_sequence)
        row = cursor.fetchone()
        if row is not None:
            human_dna = {
                'is_mutant': row[0]
            }
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
            return human_dna

def get_human_dna_statistics():
    connection = None
    human_dna_statistics = None
    try:
        connection = utils.database_utils.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM human_dna_statistics')
        row = cursor.fetchone()
        human_dna_statistics = {
            "count_mutant_dna": row[0],
            "count_human_dna": row[1],
            "ratio": float(row[2])
        }
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
            return human_dna_statistics

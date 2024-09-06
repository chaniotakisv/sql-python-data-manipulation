import configparser
import requests 
import mysql.connector

# Read/Input the .ini file
config = configparser.ConfigParser()
input_directory = '[your_home_directory]/input.ini'
config.read(input_directory)

# Extract the contents/sections from the .ini file
gene_ids = dict(config.items('gene_ids'))
domain_names = dict(config.items('domain_names'))
credentials = dict(config.items('credentials'))
file_names = dict(config.items('file_names'))

# Pass the rest.ensembl.org
ensembl_api = domain_names['ensembl_api']

# Fetch the Ensembl mouse gene id and percent identity between the human and mouse canonical proteins
def fetch_orthologs_info(human_gene_id):
    url = f"https://{ensembl_api}/homology/id/{human_gene_id}?target_species=mouse;type=orthologues;content-type=application/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        orthologs_info = []
        for homology in data:
            for hom in homology['homologies']:
                mouse_gene_id = hom['target']['id']
                percent_identity = hom['target']['perc_id']
                orthologs_info.append((mouse_gene_id, percent_identity))
        return orthologs_info
    else:
        print(f"Failed to fetch orthologs for gene ID {human_gene_id}. Status code: {response.status_code}")
        return []

# Fetch orthologs info for each human gene and print the information
for gene_name, gene_id in gene_ids.items():
    orthologs_info = fetch_orthologs_info(gene_id)
    if orthologs_info:
        print(f"Human Gene: {gene_name}, ID: {gene_id}")
        for mouse_gene_id, percent_identity in orthologs_info:
            print(f"Mouse Gene ID: {mouse_gene_id}, Percent Identity: {percent_identity}")
    else:
        print(f"No orthologs found for gene {gene_name}")

# Fetch information about the number of exons for the canonical transcript of each gene using UCSC MariaDB database
def fetch_number_of_exons(gene_name):
    try:
        # Connection to the UCSC MariaDB database
        conn = mysql.connector.connect(
                user=credentials['ucsc_user'],
                host=domain_names['ucsc_mysql'],
                port=3306,
                database='hg38',  # database name
                auth_plugin='password'  
        )
        
        cursor = conn.cursor()

        query = """
        SELECT kgXref.geneSymbol, exonCount
        FROM knownGene
        JOIN kgXref ON knownGene.name = %s
        JOIN knownCanonical ON knownGene.name = knownCanonical.transcript
        JOIN knownToGencodeV38 ON knownGene.name = knownToGencodeV38.name
        GROUP BY exonCount;
        """

        cursor.execute(query, (gene_name,))

        # Fetch the results
        exon_counts = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()
        return exon_counts
    
    except mysql.connector.Error as error:
        print("Error occurred while fetching exon counts:", error)
        return None

# Create and open the TSV file in write mode
tsv_file_path = '[your_home_directory]/coding_test.tsv'  # output path for TSV file
with open(tsv_file_path, 'w') as tsv_file:

    # Headers of TSV file
    tsv_file.write("gene_name\tensembl_gene_id\tensembl_mouse_gene_id\tpct_idty\tnumber_of_exons\n")

    # Write each gene and its orthologs with percent identity and number of exons to the TSV file
    for gene_name, gene_id in gene_ids.items():
        orthologs_info = fetch_orthologs_info(gene_id)
        num_of_exons = fetch_number_of_exons(gene_name)
        if orthologs_info:
            for mouse_gene_id, percent_identity in orthologs_info:
                tsv_file.write(f"{gene_name}\t{gene_id}\t{mouse_gene_id}\t{percent_identity}\t{num_of_exons}\n")
        else:
            tsv_file.write(f"{gene_name}\t{gene_id}\tNo orthologs found\tN/A\n")

print(f"TSV file saved to: {tsv_file_path}")
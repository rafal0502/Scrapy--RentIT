import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess



def run_azure():
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(connection_string='DefaultEndpointsProtocol=https;AccountName=flatscontainer;AccountKey=kx/bb+HLnwGFXwvT194g3Gl5EY8kM2OlG/Wb8El8b4yd/rjlcpqHHVjSJd0XG53DOxH4qiHszcU+sxogA52suA==;EndpointSuffix=core.windows.net', account_key='kx/bb+HLnwGFXwvT194g3Gl5EY8kM2OlG/Wb8El8b4yd/rjlcpqHHVjSJd0XG53DOxH4qiHszcU+sxogA52suA==')

        # Create a container.
        container_name ='datafromscraper'
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        # Create a file in Documents to test the upload and download.
        local_path=os.path.expanduser("..\dane") # <----------- ścieżka do pliku
        local_file_name ="flats_final.csv" # <---------------- nazwa pliku 
        full_path_to_file =os.path.join(local_path, local_file_name)

        #print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob " + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)
        
    except Exception as e:
        print(e)

run_azure()
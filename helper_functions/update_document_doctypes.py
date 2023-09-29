import requests
import json


def main():
    response = requests.get('http://localhost:7071/api/GetDocuments')
    all_documents = json.loads(response.content)
    i = 0
    for document in all_documents:
        response = requests.post(
            url=f"http://localhost:7071/api/UpdateDocument?document_id={document['id']}",
        )
        i = i + 1
        print(
            f"Updated document with ID {document['id']} ({i}/{len(all_documents)})")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

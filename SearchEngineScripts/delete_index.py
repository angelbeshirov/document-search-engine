from elasticsearch import Elasticsearch

def main():
    es = Elasticsearch()
    es.indices.delete(index='library_index', ignore=[400])
    print("Index deleted successfully!")

if __name__ == '__main__':
    main()
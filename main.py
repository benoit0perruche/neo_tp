from parsers import DjsParser
from py2neo import authenticate, Graph, Path

if __name__ == '__main__':

    authenticate("127.0.0.1:7474", "neo4j", "neotp")
    graph = Graph("http://127.0.0.1:7474/db/data/")
    tx = graph.cypher.begin()

    djs_parser = DjsParser("raw_data/djs.csv")
    for dj in djs_parser.read_csv():
        tx.append("CREATE (dj:Dj {dj_id:{dj_id}, name:{name}, soundcloud_url:{soundcloud_url}}) RETURN dj",
                  dj_id=dj.dj_id,
                  name=dj.name,
                  soundcloud_url=dj.soundcloud_url)
    tx.commit()
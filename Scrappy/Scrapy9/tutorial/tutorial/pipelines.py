# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from tutorial.models import Quote, Author, Tag, db_connect, create_table

class TutorialPipeline:

    def __init__(self):
        """
        Initialize database connection and session maker
        Create Table
        """

        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker

    def process_item(self, item, spider):

        """
        Save Quotes in the database
        This method is called for every pipeline component
        """

        session = self.session()
        quote = Quote()
        author = Author()
        tag = Tag()

        author.name = item["author_name"]
        author.birthday = item["author_birthday"]
        author.bornlocation =  item["author_bornlocation"]
        author.bio = item["author_bio"]

        quote.quote_content = item["quote_content"]

        #check whether an author is exist
        exist_author = session.query(Author).filter_by(name = author.name).first()

        if exist_author is not None:
            quote.author = exist_author
        
        else:
            quote.author = author
        

        #check whether the current quote has tags or not

        if "tags" in item:

            for tag_name in item["tags"]:

                tag = Tag(name=tag_name)

                #check whether the current tag already exists in the database
                exists_tag = session.query(Tag).filter_by(name=tag.name).first()
                if exists_tag is not None:
                    tag = exists_tag
                
                quote.tags.append(tag)
        
        try:
            session.add(quote)
            session.commit()
        
        except:
            session.rollback()
            raise 

        finally:
            session.close()
            
        return item

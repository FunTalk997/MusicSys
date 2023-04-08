# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MusicSysSpiderPipeline:
    """
        同步插入数据库
        """

    def __init__(self, host, db, port, user, password):
        self.connect = pymysql.connect(host=host, user=user, password=password, port=port, db=db, charset='utf8')
        self.cursor = self.connect.cursor()
        logging.info('数据库连接成功 => 主机：%s', host + ' 端口：' + str(port) + '数据库：' + db)

    @classmethod
    def from_crawler(cls, crawler):
        db_name = crawler.settings.get('DB_SETTINGS')
        db_params = db_name.get('db1')
        return cls(
            host=db_params.get('host'),
            db=db_params.get('db'),
            user=db_params.get('user'),
            password=db_params.get('password'),
            port=db_params.get('port'),
        )

    def process_item(self, item, spider):
        table_fields = item.get('table_fields')
        table_name = item.get('table_name')
        if table_fields is None or table_name is None:
            raise Exception('必须要传表名table_name和字段名table_fields，表名或者字段名不能为空')
        values_params = '%s, ' * (len(table_fields) - 1) + '%s'
        keys = ', '.join(table_fields)
        values = ['%s' % str(item.get(i, '')) for i in table_fields]
        insert_sql = 'insert into %s (%s) values (%s)' % (table_name, keys, values_params)
        try:
            self.connect.ping(reconnect=True)
            self.cursor.execute(insert_sql, tuple(values))
            logging.info("数据插入成功 => " + '1')
        except Exception as e:
            logging.error("执行sql异常 => " + str(e))
            pass
        finally:
            # 要提交，不提交无法保存到数据库
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()
        self.cursor.close()
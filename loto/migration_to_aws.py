import boto3
import db_mysql
from datetime import datetime


class MigrationToAws:

    def __init__(self):
        self.mysql_db = db_mysql.Loto()

        self.cluster_arn = 'arn:aws:rds:ap-northeast-1:724365301150:cluster:theta-db-first'
        self.secret_arn = 'arn:aws:secretsmanager:ap-northeast-1:724365301150:secret:theta-inc-first-IMdrRy'

        self.rds_data = boto3.client('rds-data')

    def create_table(self):
        sql = """
            create table lotteries
            (
                id mediumint auto_increment primary key,
                lottery_date date,
                times int,
                num_set varchar(256),
                kind int,
                one_unit int,
                one_amount bigint,
                two_unit int,
                two_amount bigint,
                three_unit int,
                three_amount bigint,
                four_unit int,
                four_amount bigint,
                five_unit int,
                five_amount bigint,
                six_unit int,
                six_amount bigint,
                sales bigint,
                carryover bigint,
                created_at timestamp default CURRENT_TIMESTAMP null,
                updated_at timestamp null on update CURRENT_TIMESTAMP
            );
        """
        response2 = self.rds_data.execute_statement(resourceArn=self.cluster_arn,
                                                    secretArn=self.secret_arn,
                                                    database='loto',
                                                    sql=sql)

        print(response2["numberOfRecordsUpdated"])

    def exist_check(self):
        param_value = {'name': 'lottery_date', 'value': {'stringValue': '2021-10-29'}}
        param_set = [param_value]

        # sql='insert into employees(first_name, last_name) VALUES(:firstname, :lastname)',
        sql = 'SELECT * FROM lotteries WHERE lottery_date = :lottery_date'
        response2 = self.rds_data.execute_statement(resourceArn=self.cluster_arn,
                                                    secretArn=self.secret_arn,
                                                    database='loto',
                                                    sql=sql,
                                                    parameters=param_set)

        # print(response2["numberOfRecordsUpdated"])
        print(response2["records"])

    def test_insert(self):

        lottery_data = self.mysql_db.get_lotteries_data_from_target_date('2021-10-29')

        lottery_data.print()

        str_lottery_date =  None if lottery_data.created_at is None else datetime.strftime(lottery_data.lottery_date, '%Y-%m-%d')
        str_created_at = None if lottery_data.created_at is None else datetime.strftime(lottery_data.created_at, '%Y-%m-%d %H:%M:%S')
        # str_updated_at = None if lottery_data.updated_at is None else datetime.strftime(lottery_data.updated_at, '%Y-%m-%d %H:%M:%S')
        str_updated_at = None if lottery_data.updated_at is None else datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        param1 = {
            'name': 'lottery_data', 'value': {'stringValue': str_lottery_date},
            'name': 'times', 'value': {'longValue': lottery_data.times},
            'name': 'num_set', 'value': {'stringValue': lottery_data.num_set},
            'name': 'kind', 'value': {'longValue': lottery_data.kind},
            'name': 'one_unit', 'value': {'longValue': lottery_data.one_unit},
            'name': 'one_amount', 'value': {'longValue': lottery_data.one_amount},
            'name': 'two_unit', 'value': {'longValue': lottery_data.two_unit},
            'name': 'two_amount', 'value': {'longValue': lottery_data.two_amount},
            'name': 'three_unit', 'value': {'longValue': lottery_data.three_unit},
            'name': 'three_amount', 'value': {'longValue': lottery_data.three_amount},
            'name': 'four_unit', 'value': {'longValue': lottery_data.four_unit},
            'name': 'four_amount', 'value': {'longValue': lottery_data.four_amount},
            'name': 'five_unit', 'value': {'longValue': lottery_data.five_unit},
            'name': 'five_amount', 'value': {'longValue': lottery_data.five_amount},
            'name': 'six_unit', 'value': {'longValue': lottery_data.six_unit},
            'name': 'six_amount', 'value': {'longValue': lottery_data.six_amount},
            'name': 'sales', 'value': {'longValue': lottery_data.sales},
            'name': 'carryover', 'value': {'longValue': lottery_data.carryover},
            'name': 'created_at', 'value': {'stringValue': str_created_at},
            'name': 'updated_at', 'value': {'stringValue': str_updated_at}
        }
        param1 = {'name': 'lottery_date', 'value': {'stringValue': str_lottery_date}}
        param2 = {'name': 'times', 'value': {'longValue': lottery_data.times}}
            # 'name': 'num_set', 'value': {'stringValue': lottery_data.num_set},
            # 'name': 'kind', 'value': {'longValue': lottery_data.kind}
        # }
        paramSet = [param1, param2]

        # sql='insert into employees(first_name, last_name) VALUES(:firstname, :lastname)',
        sql = """
           INSERT INTO lotteries(
              lottery_date, times, num_set, kind
              , one_unit, one_amount, two_unit, two_amount
              , three_unit, three_amount, four_unit, four_amount
              , five_unit, five_amount, six_unit, six_amount
              , sales, carryover, created_at, updated_at)
            VALUES (
              :lottery_date, :times, :num_set, :kind
              , :one_unit, :one_amount, :two_unit, :two_amount
              , :three_unit, :three_amount, :four_unit, :four_amount
              , :five_unit, :five_amount, :six_unit, :six_amount
              , :sales, :carryover, :created_at, :updated_at)
        """
        # sql = 'INSERT INTO lotteries( lottery_date, times, num_set, kind ) VALUES( :lottery_date, :times, :num_set, :kind )'
        sql = 'INSERT INTO lotteries( lottery_date, times ) VALUES( :lottery_date, :times )'

        response2 = self.rds_data.execute_statement(resourceArn=self.cluster_arn,
                                                    secretArn=self.secret_arn,
                                                    database='loto',
                                                    sql=sql,
                                                    parameters=paramSet)

        print(response2["numberOfRecordsUpdated"])


if __name__ == '__main__':
    migration_aws = MigrationToAws()
    migration_aws.exist_check()
    # migration_aws.test_insert()
    # migration_aws.create_table()
    # winning_check.execute()

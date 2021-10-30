CREATE DATABASE loto;

DROP TABLE lotteries;
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

DROP TABLE buy_tmp;
create table buy_tmp
(
    id mediumint auto_increment primary key,
    csv_id int,
    target_date date,
    times int,
    num_set varchar(256),
    kind int,
    winning bigint,
    created_at timestamp default CURRENT_TIMESTAMP null,
    updated_at timestamp null on update CURRENT_TIMESTAMP
);

DROP TABLE buy;
create table buy
(
    id mediumint auto_increment primary key,
    target_date date,
    seq int,
    times int,
    num_set varchar(256),
    kind int,
    winning bigint,
    created_at timestamp default CURRENT_TIMESTAMP null,
    updated_at timestamp null on update CURRENT_TIMESTAMP
);

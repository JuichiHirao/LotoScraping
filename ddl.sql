CREATE DATABASE loto;

DROP TABLE lotteries;
create table lotteries
(
    id mediumint auto_increment primary key,
    lottery_date date,
    times int,
    num_set varchar(256),
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


-- this is the inital schema for the database

create table if not exists T_MST_STOCK_NAME (
    STOCK_ID varchar(12) primary key,
    STOCK_NAME text not null,
    TICKER text not null
);

create table if not exists T_MST_STOCK_SECTOR (
    STOCK_ID varchar (12) primary key,
    SECTOR_NAME text not null,
    foreign key (STOCK_ID) references T_MST_STOCK_NAME (STOCK_ID)
);


create table if not exists T_MST_STOCK_DETAILS (
    STOCK_ID varchar (12) primary key,
    NSE numeric(5,2),
    MARKET_CAP numeric(5,2),        -- in Crores Rs
    P_E numeric(5,2),
    BOOK_VALUE numeric(5,2),
    DIVIDEND numeric(3,2),
    EPS numeric(5,2),               -- earnings per share
    DIVIDEND_YIELD numeric(3,2),
    FACE_VALUE numeric(5,2),
    foreign key (STOCK_ID) references T_MST_STOCK_NAME (STOCK_ID)
);



create table if not exists T_MST_DIVIDEND (
    STOCK_ID varchar (12) primary key,
    DIVIDEND_YEARLY smallint,
    year1 numeric(3,2),
    year2 numeric(3,2),
    year3 numeric(3,2),
    year4 numeric(3,2),
    year5 numeric(3,2),
    foreign key (STOCK_ID) references T_MST_STOCK_NAME (STOCK_ID)
);


create table if not exists T_TRANS_BALANCESHEET (
    STOCK_ID varchar (12) primary key,
    TOTAL_RESOURCES_SURPLUS float,
    TOTAL_SHAREHOLDERS_FUND float,
    NON_CURRENT_LIABILITIES float,
    CURRENT_LIABILITIES float,
    TOTAL_CAPITAL_LIABILITIES float,
    NON_CURRENT_ASSETS float,
    CURRENT_ASSETS float,
    TOTAL_ASSETS float,
    foreign key (STOCK_ID) references T_MST_STOCK_NAME (STOCK_ID)
);


create table if not exists T_TRANS_STOCK_HOLDINGS (
    STOCK_ID varchar (12) primary key,
    PROMOTER numeric(3,2),
    FII_FPI numeric(3,2),
    FINANCIAL_INSTITUTIONS numeric(3,2),
    INSURANCE_COMPANY numeric(3,2),
    MF numeric(3,2),
    OTHER_DLL numeric(3,2),
    OTHERS numeric(3,2),
    TOTAL numeric(3,2),
    foreign key (STOCK_ID) references T_MST_STOCK_NAME (STOCK_ID)
);


create table if not exists T_TRANS_HISTORIC_DATA (
    STOCK_ID varchar (12),
    date TIMESTAMP primary key,
    OPENING numeric(5,2),
    HIGH numeric(5,2),
    LOW numeric(5,2),
    CLOSING numeric(5,2),
    VOLUME int,
    foreign key (STOCK_ID) references T_MST_STOCK_NAME (STOCK_ID)
);

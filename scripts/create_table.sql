create table user(
  id int not null auto_increment,
  name varchar(255),
  primary key (id)
);
insert into user (name) values ('foo');

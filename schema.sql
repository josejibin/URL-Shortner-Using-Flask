drop table if exists url;
create table url(
  id integer primary key autoincrement,
  original_url text not null,
  shortened_url text not null
);

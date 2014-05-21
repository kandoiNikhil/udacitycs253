create or replace function random() returns void as
$$   
declare
i record;

begin 

insert into student values(4001,'qwe','123',2);
for i in select * from course loop
	update course set cfees=1.1*cfees;
end loop;
insert into student values(4001,'qwe','123',2);

end;

$$ language plpgsql;

select random();

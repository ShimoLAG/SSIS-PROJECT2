use mydb;

create table Student(
studentID varchar(50) primary key,
studentName varchar (50) not null, 
coursecode varchar(50), 
year ENUM('1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year', 'Irregular') NOT NULL,
gender ENUM('Female', 'Male', 'Other') NOT NULL
);

create table Course(
coursecode varchar(50) primary key,
course_name varchar(50)
);

alter table Student
add constraint coursecode
foreign key (coursecode) references Course(coursecode);

select * from Student;
select * from Course;

drop table course;
drop table student;

insert into Student
values ("2020-0001","lebron james", "BSCS", "2nd Year", "male"),
("2020-0002","nagta", "BSCA", "3rd Year", "male"),
("2020-0053","Jeal", "BSCS", "3rd Year", "female"),
("2020-0052", "Humaira Cameron", "BSCS", "2nd Year", "Female"),
("2020-0051", "Keaton Dunlop", "BSIT", "2nd Year", "Male"),
("2020-0003", "Usmaan Contreras", "BSCS", "2nd Year", "Male"),
("2020-0004", "Rajveer Pope", "BSCS", "2nd Year", "Male"),
("2020-0005", "Safia Newman", "N/A", "2nd Year", "Female"),
("2020-0006", "Finlay Regan", "BSIT", "2nd Year", "Female"),
("2020-0007", "Maya Bourne", "BSIS", "2nd Year", "Female"),
("2020-0008", "Areebah Wade", "BSCS", "2nd Year", "Female"),
("2020-0009", "Umaiza Ramsay", "BSCS", "2nd Year", "Female"),
("2020-0010", "Trey Bull", "BSIT", "2nd Year", "Male"),
("2020-0011", "Naveed Rooney", "BSIS", "2nd Year", "Male"),
("2020-0012", "Cataleya Crane", "BSCA", "2nd Year", "Female"),
("2020-0013", "who", "BSCS", "2nd Year", "Male"),
("2020-0014", "Dillan Hirst", "BSIT", "2nd Year", "Male"),
("2020-0015", "Ahmet Knott", "BSCS", "2nd Year", "Male"),
("2020-0016", "Timur Dillard", "BSCS", "2nd Year", "Male"),
("2020-0017", "Scarlett Madden", "BSIS", "2nd Year", "Female"),
("2020-0018", "Velma Dejesus", "BSCA", "2nd Year", "Female"),
("2020-0019", "Gerrard Solomon", "BSCS", "2nd Year", "Male"),
("2020-0020", "Maxine Nolan", "BSIT", "2nd Year", "Female"),
("2020-0021", "Eva Bowes", "BSCS", "2nd Year", "Female"),
("2020-0022", "Rhiann Rhodes", "BSCS", "2nd Year", "Female"),
("2020-0023", "Amelia-Grace May", "BSIS", "2nd Year", "Female"),
("2020-0024", "Terence Bond", "BSCA", "2nd Year", "Male"),
("2020-0025", "Chardonnay Bone", "BSCS", "2nd Year", "Male"),
("2020-0026", "Kiah Churchill", "BSIT", "2nd Year", "Female"),
("2020-0027", "Derek Shaffer", "BSCS", "2nd Year", "Male"),
("2020-0028", "Maisy Maxwell", "BSCS", "2nd Year", "Female"),
("2020-0029", "Nigel Mcdonald", "BSIS", "2nd Year", "Male"),
("2020-0030", "Teo Thomas", "BSCA", "2nd Year", "Male"),
("2020-0031", "Casper Castaneda", "BSCS", "2nd Year", "Male"),
("2020-0032", "Keiran Fernandez", "BSIT", "2nd Year", "Female"),
("2020-0033", "Harmony Booker", "BSCS", "2nd Year", "Female"),
("2020-0034", "Reef Sadler", "BSCS", "2nd Year", "Male"),
("2020-0035", "Nichole Johnston", "BSIS", "2nd Year", "Female"),
("2020-0036", "Kavita Storey", "BSCA", "2nd Year", "Female"),
("2020-0037", "Fynley Flower", "BSCS", "4th Year", "Female"),
("2020-0038", "Aron Huynh", "BSIT", "2nd Year", "Male"),
("2020-0039", "Blessing Munro", "BSCS", "2nd Year", "Female"),
("2020-0040", "Gracie Howard", "BSCS", "2nd Year", "Female"),
("2020-0041", "Maariya Smyth", "BSIS", "2nd Year", "Female"),
("2020-0042", "Sami Christie", "BSCA", "2nd Year", "Female"),
("2020-0043", "Crystal Noble", "BSCS", "2nd Year", "Female"),
("2020-0044", "Kaylie Owens", "BSIT", "2nd Year", "Female"),
("2020-0045", "Ricardo Milos", "BSCS", "2nd Year", "Male"),
("2020-0046", "Tess Dunne", "BSCS", "2nd Year", "Female"),
("2020-0047", "Archibald Robson", "BSIS", "2nd Year", "Male"),
("2020-0048", "Connah Knights", "BSCA", "2nd Year", "Male"),
("2020-0050", "Pascal Humphrey", "BSIT", "2nd Year", "Male"),
("2020-1699", "Knee Garbanzos", "BSCS", "Irregular", "Other"),
("2020-1453", "Darkafterburn123", "BSCA", "4th Year", "Female");

insert into Course
values("BSCA", "bachelor of computer applications"),
("BSIT", "bachelor of science in information technology"),
("BSCS", "Bachelor of science in computer studies"),
("BSIS", "Bachelor of science in information Systems"),
("N/A", "N/A");

SELECT * FROM Student
WHERE coursecode = "BSCS";


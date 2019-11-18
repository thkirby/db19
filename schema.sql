drop table if exists Customer;
create table Customer(
    custid serial primary key not null,
    firstName varchar(50) not null,
    lastName varchar(50) not null
    paymentInfo serial not null,
    phoneNumber int not null,
    email varchar(50) not null,
    
);

drop table if exists Submission;
create table Submission(
    subID serial primary key not null,
    custID int not null,  
    typeofSub varchar(50) not null,
);

drop table if exists Car;
create table Car(
    carID serial primary key not null,
    latitude float not null,
    longitude float not null,
    statusOf varchar(100) not null,
);

drop table if exists Reservation;
create table Reservation(
    timeOfRes timestamp with time zone not null default now(),
    place varchar(50) not null,
    resID serial primary key not null,
    custID serial primary key not null references Customer,
    carID serial primary key not null references Car
);

drop table if exists Incident;
create table Incident(
    incidentID int primary key not null,
    carID serial primary key not null references Car,
    custid serial primary key not null references Customer,

);

drop table if exists Rides;
create table Rides(
    custid serial primary key not null references Customer,
    carID serial primary key not null references Car,
    startTime timestamp with time zone not null default now(),
    endTime timestamp with time zone,
    dateOfRide timestamp with time zone
);

drop table if exists Stations;
create table Stations(
    stationID serial primary key not null,
    available boolean not null,
    stationLocation varchar(50) not null,
    energyConsumption float not null,
);

drop table if exists Routes;
create table Routes(
    routeID serial primary key,
    carID int not null,
    startLocation varchar(100) not null,
    endLocation varchar(100) not null,
);

drop table if exists traffic;
create table traffic(
    density int,
    carID serial primary key not null references Car,
    routeID serial primary key references Routes
);


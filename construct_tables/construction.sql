

-- Create the Database teams for the following commands: 
CREATE DATABASE teams
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;




CREATE TABLE entity (
        entity_id SERIAL PRIMARY KEY,
        entity_name VARCHAR(255) NOT NULL,
        UNIQUE(entity_name)
    );


CREATE Table entity_time 
    (
        entity_time_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        entity_id BIGINT NOT NULL, 
        coverage integer NOT NULL
    );



CREATE TABLE team_members (
    team_id SERIAL PRIMARY KEY,
    pre_name VARCHAR(100) NOT NULL,
    sur_name VARCHAR(150) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    UNIQUE(full_name),
    email text,
    user_id text NOT NULL,
    legal_entity_id BIGINT,
    department_entry_date DATE,
    status VARCHAR(20)
);


CREATE TABLE ods (
    od_id SERIAL PRIMARY KEY,
    od_name VARCHAR(10) NOT NULL,
    UNIQUE(od_name)
);



CREATE TABLE team_info (
    team_info_id SERIAL PRIMARY KEY,
    team_id INTEGER NOT NULL,
    FOREIGN KEY (team_id)
        REFERENCES team_members (team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    year INTEGER NOT NULL,
    contract INTEGER NOT NULL,
    working_month INTEGER NOT NULL,
    entity_id BIGINT NOT NULL, 
    FOREIGN KEY (entity_id)
        REFERENCES entity (entity_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    activity VARCHAR(255),
    UNIQUE (year, team_id)
);


CREATE TABLE founding_sources (
    founding_source_id SERIAL PRIMARY KEY,
    founding_source VARCHAR(255) NOT NULL,
    UNIQUE(founding_source)
);





CREATE TABLE topic_class (
    topic_class_id SERIAL PRIMARY KEY,
    topic_class VARCHAR(255) NOT NULL,
    UNIQUE(topic_class)
);




CREATE TABLE project (
    project_id SERIAL PRIMARY KEY,
    funding_id BIGINT NOT NULL,
    FOREIGN KEY (funding_id)
        REFERENCES founding_sources (founding_source_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    topic VARCHAR(255) NOT NULL,
    topic_class_id BIGINT NOT NULL,
    FOREIGN KEY (topic_class_id)
        REFERENCES topic_class (topic_class_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    argus_enabled VARCHAR(5) NOT NULL,
    way_charging VARCHAR(10) NOT NULL,
    cost_center_respon VARCHAR(255),
    start_date DATE,
    end_date DATE,
    difficulty integer,
    project_status VARCHAR(50),
    project_description TEXT,
    project_goals TEXT
);


CREATE TABLE project_team_members (
    project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
    team_id int REFERENCES team_members (team_id) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (project_id, team_id)
    );



CREATE TABLE project_deadlines (
    project_deadlines_id SERIAL PRIMARY KEY,
    project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
    deadline_date DATE,
    deadline_text VARCHAR(255),
    UNIQUE (deadline_date, deadline_text)
);


CREATE Table project_budget_planning 
    (
        pbp_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        project_id integer NOT NULL,
        FOREIGN KEY (project_id) 
            REFERENCES project (project_id) 
            ON UPDATE CASCADE ON DELETE CASCADE,
        budget integer NOT NULL,
        UNIQUE (year, project_id)
    );


CREATE Table project_time_budget 
    (
        ptb_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        month integer NOT NULL,
        team_id INTEGER NOT NULL,
        FOREIGN KEY (team_id)
            REFERENCES team_members (team_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        working_days integer,
        working_booking float,
        project_id integer NOT NULL,
        FOREIGN KEY (project_id) 
            REFERENCES project (project_id) 
            ON UPDATE CASCADE ON DELETE CASCADE,
        UNIQUE (year, month, team_id, project_id)
    );



CREATE Table team_year_project_budget 
    (
        ttpb_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        team_id INTEGER NOT NULL,
        FOREIGN KEY (team_id)
            REFERENCES team_members (team_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        project_id INTEGER NOT NULL,
        FOREIGN KEY (project_id)
            REFERENCES project (project_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        project_yearly_budget INTEGER NOT NULL,
        UNIQUE (year, team_id, project_id)
    );


CREATE Table project_costcenter
    (
        pc_id SERIAL UNIQUE PRIMARY KEY,
        project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
        costcenter VARCHAR(50) NOT NULL
    );


CREATE Table active_project_person_costcenter
    (
        appc_id SERIAL UNIQUE PRIMARY KEY,
        project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
        team_id int REFERENCES team_members (team_id) ON UPDATE CASCADE ON DELETE CASCADE,
        costcenter VARCHAR(100) NOT NULL,
        UNIQUE (project_id, team_id)
    );






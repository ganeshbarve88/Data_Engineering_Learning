Install VS Code and Create Repo in Github

git clone : 
    git clone https://github.com/username/repository.git

Install Git :
    sudo apt update
    sudo apt install git

Install Python : 
    sudo apt install
    sudo apt upgrade
    python3 --version
    sudo apt install python3

Install Pip :
    sudo apt update
    sudo apt install python3-pip
    pip3 --version

Vertual Env : 
    sudo apt install python3-venv
    python3 -m venv dbt-env
    source dbt-env/bin/activate

Install Power DBT User in VS code extension

Install DBT Package :
    pip install dbt-core dbt-postgres

==============Installing DB================

Sqlserver :
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
# For Ubuntu 24.04
curl -fsSL https://packages.microsoft.com/config/ubuntu/24.04/mssql-server-2022.list | sudo tee /etc/apt/sources.list.d/mssql-server-2022.list

sudo apt-get update
sudo apt-get install -y mssql-server

sudo /opt/mssql/bin/mssql-conf setup

systemctl status mssql-server --no-pager

curl -fsSL https://packages.microsoft.com/config/ubuntu/24.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update

sudo apt-get install -y mssql-tools18 unixodbc-dev

echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

sqlcmd -S localhost -U sa -P 'YourStrongPassword' -C

SELECT @@VERSION;
GO


PostGresSQL :

sudo apt update

sudo apt install postgresql postgresql-contrib

systemctl status postgresql

sudo -i -u postgres

createuser --interactive --pwprompt dbt_user

createdb -O dbt_user dbt_learning

exit

loading Sample Data :

wget https://github.com/devrimgunduz/pagila/raw/master/pagila-insert-data.sql
wget https://github.com/devrimgunduz/pagila/raw/master/pagila-schema.sql
sudo -u postgres psql -d dbt_learning -f pagila-schema.sql
sudo -u postgres psql -d dbt_learning -f pagila-insert-data.sql
sudo -u postgres psql -d dbt_learning -c "GRANT USAGE ON SCHEMA public TO dbt_user; GRANT SELECT ON ALL TABLES IN SCHEMA public TO dbt_user; GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO dbt_user;"

# Log in as dbt_user
psql -h localhost -U dbt_user -d dbt_learning

# List tables to see if they are populated
\dt
SELECT count(*) FROM film;


===Creating first project :

dbt init my_first_project

During the setup wizard:

When it asks for the database, select the number for postgres.

For host, type localhost.

For port, type 5432 (this is the default for Postgres).

For user, use dbt_user (the one we created in Phase 2).

For password, enter the password you set.

For dbname, use dbt_learning.

For schema, use public.

dbt debug


Installing GUI : 

sudo snap install dbeaver-ce --classic

dbeaver-ce &



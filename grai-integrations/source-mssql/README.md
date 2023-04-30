# Grai SQL Server Integration

The SQL Server integration synchronizes metadata from your SQL Server database into your Grai data lineage graph.

Tests assume you have working installation of pyodbc and a supported
ODBC driver installed on your host machine.

## Installation Notes

Installing ODBC drivers can be particularly tricky on M1 machines.
You'll need to install the unixodbc drivers through brew first

```bash
    brew install unixodbc
```

You can attempt installing pyodbc directly at this point though I was forced to
set LDFLAGS and CPPFlags in my bashrc/zshrc file, i.e.

```bash
export LDFLAGS="$LDFLAGS -L$(brew --prefix unixodbc)/lib"
export CPPFLAGS="$CPPFLAGS -I$(brew --prefix unixodbc)/include"
```

At this point you should be able to `pip install pyodbc` successfully
and import the package from within python. However, you'll still require an
ODBC driver in order to connect with an MS SQL server. There are multiple options
for potential drivers but ODBC 18 from Microsoft has worked in testing.

```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```

If you continue to experience issues you might try creating these symlinks
below.

```
sudo ln -s /opt/homebrew/etc/odbcinst.ini /etc/odbcinst.ini
sudo ln -s /opt/homebrew/etc/odbc.ini /etc/odbc.ini
```

When installing locally, if you get an error like `ImportError: dlopen(/opt/homebrew/lib/python3.11/site-packages/pyodbc.cpython-311-darwin.so, 0x0002): symbol not found in flat namespace (_SQLAllocHandle)`, you can try uninstalling `pip uninstall pyodbc` and then reinstall with build `pip install --no-binary :all: pyodbc`.

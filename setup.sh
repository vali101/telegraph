# Setup venv
virtualenv televenv
source televenv/bin/activate

# Install dependency for Language Detection 
# install libicu (keg-only)
brew install pkg-config icu4c

# let setup.py discover keg-only icu4c via pkg-config
export PATH="/usr/local/opt/icu4c/bin:/usr/local/opt/icu4c/sbin:$PATH"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/opt/icu4c/lib/pkgconfig"

# Install dependecys python 
pip install -r requirements.txt

echo "Done with Setup"



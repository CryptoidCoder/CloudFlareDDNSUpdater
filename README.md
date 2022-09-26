# Cloudflare DDNS Updater

## This Will Update Your Cloudflare DNS With Your Devices Public IP

### Usage:
`python main.py`


### Setup:
1) You Need To Initially Run `main.py` To Setup The Environmental Config.
2) You Need To Set `main.py` To Run On Startup.

- Linux:
- - `crontab -e`
- - Then Add The Following:
- - - `@reboot python3 /path/to/this/directory/main.py`

- Windows:
- - Copy The Included `CloudFlareDDNSUpdater.cmd` File Into `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
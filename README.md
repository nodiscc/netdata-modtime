# netdata-modtime

Check/graph last modification time of files and directories

![](https://i.imgur.com/FQqBT7o.png)

This is a `python.d` plugin for [netdata](https://my-netdata.io/).

Maximum acceptable age of each watched file can be configured, alarms will be raised if the last modification time is older than this value.


## Installation

```bash
# clone the repository
git clone https://gitlab.com/nodiscc/netdata-modtime

# edit configuration values in these files (update interval, watched files, alarm thresholds...)
nano netdata-modtime/python.d_modtime.conf
nano netdata-modtime/health.d_modtime.conf

# copy files in place
netdata_install_prefix="/opt/netdata" # if netdata is installed from binary/.run script
netdata_install_prefix="" # if netdata is installed from OS packages
sudo cp netdata-modtime/modtime.chart.py $netdata_install_prefix/usr/libexec/netdata/python.d/
sudo cp netdata-modtime/python.d_modtime.conf $netdata_install_prefix/etc/netdata/python.d/modtime.conf
sudo cp netdata-modtime/health.d_modtime.conf $netdata_install_prefix/etc/netdata/health.d/modtime.conf

# restart netdata
systemctl restart netdata

```

## Configuration

- Files for which time since last modification should bea measured, and chart refresh time/common `python.d` plugin options can be changed in [`$netdata_install_prefix/etc/netdata/python.d/modtime.conf`](python.d_modtime.conf)
- Alarm settings can be changed in [`$netdata_install_prefix/etc/netdata/health.d/modtime.conf`](health.d_modtime.conf)

## Usage

To monitor time since last successful execution of a cron job or other scheduled task, have it update the modification time of a file on successful execution, for example:

```bash
# my daily backup job
0 1 * * * root rsnapshot daily && touch /var/log/rsnapshot_last_success
```

[Configure](python.d_modtime.conf) the plugin to watch this file:

```yaml
last_rsnapshot_success:
  path: '/var/log/rsnapshot_last_success'
```

[Configure](health.d_modtime.conf) an alarm/notification when the file age exceeds a threshold.

```yaml
# Raise a warning when the file is older than 24h30min
# Raise a critical alert when older than 25h
  alarm: modtime_last_rsnapshot_success
     on: modtime_last_rsnapshot_success.file_age
   calc: $file_age
  every: 10s
   warn: $this > 88200
   crit: $this > 90000
  units: seconds
   info: time since last modification
     to: sysadmin
```

## Debug

To debug this plugin:

```bash
$ sudo su -s /bin/bash netdata
$ $netdata_install_prefix/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace modtime
```


## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-modtime
- https://gitlab.com/nodiscc/netdata-modtime


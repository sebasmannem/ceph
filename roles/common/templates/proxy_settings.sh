# KLOWED Proxy exports
export http_proxy={{ proxy_server }}
export https_proxy="${http_proxy}"
export ftp_proxy="${http_proxy}"
export no_proxy="localhost,127.0.0.1,$(hostname),.$(hostname -d)"


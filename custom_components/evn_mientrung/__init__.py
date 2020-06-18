from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.helpers.event import track_time_interval
from homeassistant.util.dt import utcnow
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

CONF_SCAN_INTERVAL_MINUTE = "scan_interval_minute"
DOMAIN = "evn_mientrung"
CONF_USER_ID = "evn_id"
COMPONENT_TYPES = ["sensor"]

SCAN_INTERVAL = 15 #minute

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USER_ID): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL_MINUTE, default=SCAN_INTERVAL): cv.time_period,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
  evn_id = config[DOMAIN][CONF_USER_ID]
  scan_interval = config[DOMAIN][CONF_SCAN_INTERVAL_MINUTE]

  if DOMAIN not in hass.data:
    hass.data[DOMAIN] = {}
  hass.data[DOMAIN][evn_id] = {}

  for component in COMPONENT_TYPES:
    discovery.load_platform(hass, component, DOMAIN, {}, config)

  def update(event_time):
    dispatcher_send(hass, "{}_updated".format(DOMAIN), evn_id)

  update(utcnow())
  track_time_interval(hass, update, scan_interval*60)
  return True

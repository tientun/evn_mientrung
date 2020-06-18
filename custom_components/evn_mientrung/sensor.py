import asyncio
import logging

from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.helpers.entity import Entity
from homeassistant.util import slugify
from homeassistant.core import callback
import requests
from bs4 import BeautifulSoup as BS

DOMAIN = "evn_mientrung"
CONF_USER_ID = "evn_id"
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    for user, data in hass.data[DOMAIN].items():
        add_entities([EvnSensor(user, data)])
    
class EvnSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self, evn_id, data):
        """Initialize the sensor."""
        self.entity_id = ENTITY_ID_FORMAT.format(
            "{}_{}".format("evn", slugify(evn_id))
        )
        self._env_id = evn_id
        self._unique_id = slugify(evn_id)
        self._state = None
        self._unit_of_measurement = "kWh"
        self._name = None
        self._available = None
        self._state_attrs = {
            "name":None,
            "total":None,
            "last_check":None,
            "last_month_total":None,
            "last_month_check_date":None,
            "metter_id":None,
            "metter_type":None,
            "transformer_id":None,
            "address":None
        }

    @asyncio.coroutine
    def async_added_to_hass(self):
        """Register callbacks."""
        self.hass.helpers.dispatcher.async_dispatcher_connect(
            "evn_mientrung_updated", self.async_update_callback
        )
        self.async_update_callback(self._env_id)

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def available(self):
        """Return true when state is known."""
        return self._available

    @property
    def device_state_attributes(self):
        return self._state_attrs
    
    def get_value(self, raw_data, key):
        soup = BS(raw_data, features="html.parser")
        return soup.find('span', {'id':key}).text

    @callback
    def async_update_callback(self, env_id):
        """Update state."""
        self._available = True
        url = 'https://spider.cpc.vn/kh.aspx'
        raw_data = '__EVENTTARGET=&__CALLBACKID=basicinfokh_panel&__CALLBACKPARAM=c0:getinfo' + env_id
        response = requests.post(url, data=raw_data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, verify=False)
        data={}
        data["name"]=self.get_value(response.text, 'basicinfokh_panel_TEN_KHANG')
        data["address"]=self.get_value(response.text, 'basicinfokh_panel_DIA_CHI')
        data["transformer_id"]=self.get_value(response.text, 'basicinfokh_panel_MA_TRAM')
        data["meter_id"]=self.get_value(response.text, 'basicinfokh_panel_SERY_CTO')
        data["meter_type"]=self.get_value(response.text, 'basicinfokh_panel_METER_TYPE')
        data["last_month_total"]=self.get_value(response.text, 'basicinfokh_panel_CS_CU')
        data["last_month_check_date"]=self.get_value(response.text, 'basicinfokh_panel_NGAY_CU')
        data["total"]=self.get_value(response.text, 'basicinfokh_panel_CS_MOI')
        data["last_check"]=self.get_value(response.text, 'basicinfokh_panel_NGAY_GIO')
        data["energy"]=self.get_value(response.text, 'basicinfokh_panel_SL_MOI')

        self._state = data["energy"]
        self._unit_of_measurement = "kWh"
        self._name = data["name"]
        self._state_attrs = {
            "name":data["name"],
            "total":data["total"],
            "last_check":data["last_check"],
            "last_month_total":data["last_month_total"],
            "last_month_check_date":data["last_month_check_date"],
            "meter_id":data["meter_id"],
            "meter_type":data["meter_type"],
            "transformer_id":data["transformer_id"],
            "address":data["address"]
        }
        self.async_schedule_update_ha_state()

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

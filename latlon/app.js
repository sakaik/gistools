const form = document.getElementById('coordinate-form');
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');
const messageEl = document.getElementById('message');
const latitudeDmsEl = document.getElementById('latitude-dms');
const longitudeDmsEl = document.getElementById('longitude-dms');
const latitudeDmEl = document.getElementById('latitude-dm');
const longitudeDmEl = document.getElementById('longitude-dm');
let marker;
let mapReady = false;

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      gsiPale: {
        type: 'raster',
        tiles: ['https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '地理院タイル（淡色地図）'
      }
    },
    layers: [
      {
        id: 'gsiPale',
        type: 'raster',
        source: 'gsiPale',
        minzoom: 0,
        maxzoom: 18
      }
    ]
  },
  center: [parseFloat(longitudeInput.value), parseFloat(latitudeInput.value)],
  zoom: 4,
  attributionControl: false
});

map.addControl(new maplibregl.NavigationControl(), 'top-right');
map.addControl(new maplibregl.AttributionControl({ compact: true }));

map.on('load', () => {
  mapReady = true;
  updateView();
});

form.addEventListener('submit', (event) => {
  event.preventDefault();
  updateView();
});

[latitudeInput, longitudeInput].forEach((input) => {
  input.addEventListener('input', () => {
    if (messageEl.textContent) {
      messageEl.textContent = '';
    }
  });
});

function updateView() {
  const latitude = Number(latitudeInput.value);
  const longitude = Number(longitudeInput.value);

  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
    setMessage('緯度と経度には数値を入力してください。');
    return;
  }

  if (latitude < -90 || latitude > 90) {
    setMessage('緯度は -90 から 90 の範囲で入力してください。');
    return;
  }

  if (longitude < -180 || longitude > 180) {
    setMessage('経度は -180 から 180 の範囲で入力してください。');
    return;
  }

  clearMessage();
  latitudeDmsEl.textContent = toDms(latitude, 'lat');
  longitudeDmsEl.textContent = toDms(longitude, 'lon');
  latitudeDmEl.textContent = toDm(latitude, 'lat');
  longitudeDmEl.textContent = toDm(longitude, 'lon');

  if (mapReady) {
    if (!marker) {
      marker = new maplibregl.Marker({ color: '#2563eb' })
        .setLngLat([longitude, latitude])
        .addTo(map);
    } else {
      marker.setLngLat([longitude, latitude]);
    }

    const targetZoom = Math.max(map.getZoom(), 5);

    map.flyTo({
      center: [longitude, latitude],
      zoom: targetZoom,
      essential: true
    });
  }
}

function setMessage(text) {
  messageEl.textContent = text;
}

function clearMessage() {
  messageEl.textContent = '';
}

function toDms(value, type) {
  const direction = resolveDirection(type, value);
  const absolute = Math.abs(value);
  const degrees = Math.floor(absolute);
  const minutesFull = (absolute - degrees) * 60;
  const minutes = Math.floor(minutesFull);
  const seconds = (minutesFull - minutes) * 60;
  return `${degrees}° ${minutes}' ${seconds.toFixed(2)}" ${direction}`;
}

function toDm(value, type) {
  const direction = resolveDirection(type, value);
  const absolute = Math.abs(value);
  const degrees = Math.floor(absolute);
  const minutes = (absolute - degrees) * 60;
  return `${degrees}° ${minutes.toFixed(4)}' ${direction}`;
}

function resolveDirection(type, value) {
  if (type === 'lat') {
    return value >= 0 ? 'N' : 'S';
  }

  return value >= 0 ? 'E' : 'W';
}


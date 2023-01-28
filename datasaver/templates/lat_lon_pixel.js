/*
easiest way to conceive:
distance of 1 degree of longitude / distance of 1 degree of latitude

equivalent to:
latitude per distance / longitude per distance

if we cancel out distance
latitude / longitude
*/
function aspect(lat) {
	return Math.cos(lat / 360 * 2 * Math.PI);
}

function getPixelCoords(lat, lon, latO, lonO, pixelsPerDegree, canvas) {
	return {
		x:  (lon - lonO) * pixelsPerDegree * aspect(latO) + canvas.width  / 2,
		y: -(lat - latO) * pixelsPerDegree                + canvas.height / 2,
	};
}

function getLatLon(x, y, latO, lonO, pixelsPerDegree, canvas) {
	return {
		lat: -(y - canvas.height / 2) / pixelsPerDegree                + latO,
		lon:  (x - canvas.width  / 2) / pixelsPerDegree / aspect(latO) + lonO,
	};
}

const M_PER_DEGREE = 1e7 / 90;

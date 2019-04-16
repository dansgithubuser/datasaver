const ICON_SIZE = 4;
const CANVAS = e('canvas');
const CONTEXT = CANVAS.getContext('2d');

function drawRect(x, y, w, h, r, g, b) {
	CONTEXT.fillStyle = `rgb(${r}, ${g}, ${b})`;
	CONTEXT.fillRect(x, y, w, h);
}

function drawIcon(x, y, r = 255, g = 0, b = 0) {
	drawRect(
		x - ICON_SIZE / 2, y - ICON_SIZE / 2,
		ICON_SIZE, ICON_SIZE,
		r, g, b
	);
}

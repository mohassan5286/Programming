gain() {
    let selectedCurve = null;
    const curveTextMap = new Map();
    this.gains = {};

    const handleCurveClick = (curve) => {
        if (selectedCurve) {
            selectedCurve.stroke(selectedCurve.originalColor);
        }
        curve.originalColor = curve.stroke();
        curve.stroke('red');
        selectedCurve = curve;
        let curveKey = null;
        this.curveLineMap.forEach((value, key) => {
            if (value._id === curve._id) {
                curveKey = key;
                return;
            }
        });

        const boundingBox = curve.getClientRect();
        const curveCenterX = boundingBox.x + boundingBox.width / 2;
        const curveCenterY = boundingBox.y + boundingBox.height / 2;

        let text = curveTextMap.get(curve);
        if (!text) {
            text = new Konva.Text({
                x: curveCenterX,
                y: curveCenterY,
                text: `${document.getElementById('quantity').value}`,
                fontSize: 16,
                fontFamily: 'Arial',
                fill: 'black',
                align: 'center'
            });

            this.layer.add(text);
            curveTextMap.set(curve, text);
        } else {
            text.text(`${document.getElementById('quantity').value}`);
        }

        if (curveKey) {
            this.gains[`${curveKey}`] = document.getElementById('quantity').value;
        } else {
            console.error('Start or end ID of the curve is undefined.');
        }
    };

    this.layer.on('click', (e) => {
        const shape = e.target;
        if (shape.getClassName() === 'Arrow') {
            handleCurveClick(shape);
        }
    });

    const updateTextPositions = () => {
        curveTextMap.forEach((text, curve) => {
            const boundingBox = curve.getClientRect();
            const curveCenterX = boundingBox.x + boundingBox.width / 2;
            const curveCenterY = boundingBox.y + boundingBox.height / 2;
            text.position({ x: curveCenterX, y: curveCenterY });
        });
        this.layer.batchDraw();
    };

    this.layer.on('dragmove', updateTextPositions);

    const handleReadGainButtonClick = () => {
        if (selectedCurve) {
            const text = curveTextMap.get(selectedCurve);
            if (text) {
                text.text(`${document.getElementById('quantity').value}`);
                let curveKey;
                this.curveLineMap.forEach((value, key) => {
                    if (value._id === selectedCurve._id) {
                        curveKey = key;
                        return;
                    }
                });
                if (curveKey) {
                    this.gains[`${curveKey}`] = document.getElementById('quantity').value;
                } else {
                    console.error('Start or end ID of the curve is undefined.');
                }
                document.getElementById('quantity').value = '';
                selectedCurve.stroke(selectedCurve.originalColor);
                selectedCurve = null;
            }
        } else {
            console.log('Please select a curve arrow first.');
        }
    };

    document.getElementById('readGainButton').addEventListener('click', handleReadGainButtonClick);
}

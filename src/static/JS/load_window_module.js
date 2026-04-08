export class LoadingWindow {
    constructor() {
        this.loadingWindowBg = document.createElement('div');
        this.loadingWindowBg.id = 'loading-bg';

        const circle1 = document.createElement('div')
        circle1.id = 'circle1';
        circle1.classList.add("rotating-circle");
        this.loadingWindowBg.append(circle1);

        const circle2 = document.createElement('div')
        circle2.id = 'circle2';
        circle2.classList.add("rotating-circle");
        circle1.append(circle2);

        const circle3 = document.createElement('div')
        circle3.id = 'circle3';
        circle3.classList.add("rotating-circle");
        circle2.append(circle3);

        document.body.append(this.loadingWindowBg);
    }

    deleteWindow() {
        this.loadingWindowBg.remove();
    }
}


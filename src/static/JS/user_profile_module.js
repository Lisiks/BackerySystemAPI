export class UserProfile {

    constructor() {
        this.userProfileWindow = document.getElementById('user-profile-bg');
        
        this.userProfileWindow.addEventListener('click', (event) => {
            if (event.target === this.userProfileWindow ) {
                this.closeUserProfile();
            }
        })
    }

    openUserProfile() {
        this.userProfileWindow.style.display = 'flex';
    }

    closeUserProfile() {
        this.userProfileWindow.style.display = 'none';
    }
}
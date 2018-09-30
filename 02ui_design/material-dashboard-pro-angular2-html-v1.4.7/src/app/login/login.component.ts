import { Component, OnInit, ElementRef,ViewChild } from '@angular/core';
import { Router, NavigationExtras } from '@angular/router';

import { AuthService } from '../auth/auth.service';

declare var $: any;

@Component({
    selector: 'app-login-cmp',
    templateUrl: 'login.component.html'
})

export class LoginComponent implements OnInit {
    test: Date = new Date();
    private toggleButton: any;
    private sidebarVisible: boolean;
    private nativeElement: Node;

    @ViewChild('username') username: ElementRef;
    @ViewChild('password') password: ElementRef;

    constructor(private element: ElementRef, public authService: AuthService, public router: Router) {
        this.nativeElement = element.nativeElement;
        this.sidebarVisible = false;
    }

    ngOnInit() {
        const navbar: HTMLElement = this.element.nativeElement;
        this.toggleButton = navbar.getElementsByClassName('navbar-toggle')[0];

        setTimeout(function() {
            // after 1000 ms we add the class animated to the login/register card
            $('.card').removeClass('card-hidden');
        }, 700);
    }
    sidebarToggle() {
        const toggleButton = this.toggleButton;
        const body = document.getElementsByTagName('body')[0];
        const sidebar = document.getElementsByClassName('navbar-collapse')[0];
        if (this.sidebarVisible === false) {
            setTimeout(function() {
                toggleButton.classList.add('toggled');
            }, 500);
            body.classList.add('nav-open');
            this.sidebarVisible = true;
        } else {
            this.toggleButton.classList.remove('toggled');
            this.sidebarVisible = false;
            body.classList.remove('nav-open');
        }
    }
    login() {
        this.authService.login(this.username.nativeElement.value, this.password.nativeElement.value).subscribe(data => {
            localStorage.setItem('token', data.access_token);
            if (this.authService.isLoggedIn) {
                // Get the redirect URL from our auth service
                // If no redirect has been set, use the default
                const redirect = this.authService.redirectUrl ? this.authService.redirectUrl : '/dashboard';

                // Set our navigation extras object
                // that passes on our global query params and fragment
                const navigationExtras: NavigationExtras = {
                    queryParamsHandling: 'preserve',
                    preserveFragment: true
                };

                // Redirect the user
                this.router.navigate([redirect], navigationExtras);
            }
        });

    }
}

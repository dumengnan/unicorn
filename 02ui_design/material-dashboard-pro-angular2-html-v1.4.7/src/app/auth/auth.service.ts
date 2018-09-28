import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/delay';
import 'rxjs/add/operator/do';
import { Observable } from 'rxjs/Observable';


@Injectable()
export class AuthService {

    isLoggedIn = false;

    // store the URL so we can redirect after logging in
    redirectUrl: string;
    loginUrl: string;

    constructor(private http: HttpClient) {}


    login(username: string, password: string): Observable<boolean> {
        this.loginUrl = window.location.origin  + "/uaa/oauth/token";
        const headers = new HttpHeaders({ 'Content-Type': 'application/json' ,'Authorization' :'Basic YnJvd3Nlcjo='});
        const body = new HttpParams()
            .set('username', username)
            .set('password', password)
            .set('scope', 'ui')
            .set('grant_type', 'password');

        console.log("The username is  %s ", username);
        
        return this.http.post<boolean>(this.loginUrl, body, { headers: headers});
        // return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
    }

    logout(): void {
        this.isLoggedIn = false;
    }
}

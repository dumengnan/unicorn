import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/delay';
import 'rxjs/add/operator/do';
import { Observable } from 'rxjs/Observable';

export interface ItemResponse {
    access_token: string,
    token_type: string,
    refresh_token: string,
    expires_in: string,
    scope: string,
    jti: string    
}

@Injectable()
export class AuthService {

    isLoggedIn = false;

    // store the URL so we can redirect after logging in
    redirectUrl: string;
    loginUrl: string;

    constructor(private http: HttpClient) {}


    login(username: string, password: string): Observable<ItemResponse> {
        this.loginUrl =  "http://localhost:16003/uaa/oauth/token";
        const headers = new HttpHeaders({'Content-Type' : 'application/x-www-form-urlencoded', 
        'Authorization' : 'Basic YnJvd3Nlcjo=',
        'Access-Control-Allow-Origin' : '*'});
        let body = {
            'username':username,
            'password':password,
            'scope':'ui',
            'grant_type':'password'
        }
        // const body = new HttpParams()
        //     .set('username', username)
        //     .set('password', password)
        //     .set('scope', 'ui')
        //     .set('grant_type', 'password');

        console.log("The username is  %s %s", username, body);
        
        return this.http.post<ItemResponse>(this.loginUrl, body, { headers: headers, withCredentials: true});
        // return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
    }

    logout(): void {
        this.isLoggedIn = false;
    }
}

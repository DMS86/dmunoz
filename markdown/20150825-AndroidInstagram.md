How to add Instagram Client-side Authentication to your Android Application

I assume that you have an Android application currently working, and that your main class is called `MainActivity`. These are the steps to follow:

### 1. Create an Instagram account
### 2. [Register you application](https://instagram.com/developer/)

# 3. Register a New Client

Fill the form fields as follows. Note that in the Redurect URI field, you need to configure a redirect URI with a custom scheme. For this example, I will use *customscheme*.

* Application Name: [your-app-name]
* Description: [your-description]
* Website URL: [your-website-url]
* **Redirect URI(s): customscheme://oauth/callback/instagram/**
* Contact email: [your-email]

Then, click on the **Security** tab and uncheck the Disable implicit OAuth option. Save the Client.

# 4. Add values to the strings.xml file

After saving the Client, you will get the Client ID and Client Secret in the Instagram website. Add these values in your strings.xml file in your project:

    <string name="instagram_id">yourClientId</string>
    <string name="instagram_scheme">customscheme</string>
    <string name="instagram_secret">yourClientSecret</string>
    <string name="instagram_token">instagram_token</string>

# 5. Create the InstagramLogin Activity

Start creating an Activity in your main package. The logic for the authentication process is the following:

1. The system checks if there is an Access Token saved in SharedPreferences. 
2. If there is, it redirects to MainActivity. 
3. If not, it opens the Instagram authorization URL for the application.
4. The user authorizes the application in the browser.
5. The InstagramLogin Activity catches the Redirect URI with the *customscheme* from Instagram and gets the token.
6. The InstagramLogin Activity saves the token in SharedPreferences and redirects to MainActivity.

These will be the methods that the Activity will need for the OAuth 2.0 Client-Side authentication:

    public class InstagramLogin extends Activity {
        private String TAG = "InstagramLogin";

        @Override
        public void onCreate(Bundle savedInstanceState) {
        }

        @Override
        protected void onNewIntent(Intent intent) {
        }

        private void handleAccessToken(Intent intent) {
        }

        private void redirectToMainActivity() {
        }
    }

## 5.1. onCreate method

In this method, the Activity makes the first 3 steps in the process described above.

        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            Log.d(TAG, "onCreate");

            // Try to get Access Token from SharedPreferences
            SharedPreferences settings = PreferenceManager
                    .getDefaultSharedPreferences(getApplicationContext());
            String auth_token_string = settings.getString(
                    getApplicationContext().getString(R.string.instagram_token),
                    "");

            // Check if Access Token exists
            if (auth_token_string.compareTo("") == 0) {
                // Construct the Instagram Authentication URL based on the strings.xml variables
                String instagramUrl = "https://instagram.com/oauth/authorize/?client_id=" +
                        getApplicationContext().getString(R.string.instagram_id) +
                        "&redirect_uri=" +
                        getApplicationContext().getString(R.string.instagram_scheme) +
                        "%3A%2F%2Foauth%2Fcallback%2Finstagram%2F&response_type=token";

                // Go to the URL
                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(instagramUrl));
                startActivity(browserIntent);
            } else {
                redirectToMainActivity();
            }
        }

## 5.2. onNewIntent method

This method is called when the `Intent` is created in the `onCreate` method. The new Intent will be the one that will listen to the Redirect URI from the Instagram Authentication URL Response.

        @Override
        protected void onNewIntent(Intent intent) {
            Log.d(TAG, "onNewIntent");
            super.onNewIntent(intent);
            handleAccessToken(intent);
        }

## 5.3. handleAccessToken method

This method gets the token from the Redirect URI and saves it in `SharedPreferences`.

        private void handleAccessToken(Intent intent) {
            Log.d(TAG, "handleAccessToken");
            Uri uri = intent.getData();

            // check if the response uri starts with the custom scheme name
            if (uri != null && uri.toString().startsWith(
                    getApplicationContext().getString(R.string.instagram_scheme))) {
                String accessToken;
                if (uri.getFragment() != null) {
                    // gets access token and saves it in SharedPreferences
                    accessToken = uri.getFragment().replace("access_token=", "");
                    SharedPreferences settings = PreferenceManager
                            .getDefaultSharedPreferences(getApplicationContext());
                    SharedPreferences.Editor editor = settings.edit();
                    editor.putString(getApplicationContext().getString(R.string.instagram_token),
                            accessToken);
                    editor.apply();
                    Log.d(TAG, "Found access token: " + accessToken);

                    redirectToMainActivity();
                } else {
                    Log.d(TAG, "Access token not found. URI: " + uri.toString());
                    // Handle error here
                }
            }
        }

## 5.4. redirectToMainActivity method

This method starts the new MainActivity and finishes the InstagramLogin Activity.

        private void redirectToMainActivity() {
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
            finish();
        }

# 6. Android Manifest

In this file, you need to add an Intent Filter to the InstagramLogin Activity. According to the [Docs](http://developer.android.com/guide/components/intents-filters.html), an intent filter is an expression in an app's manifest file that specifies the type of intents that the component would like to receive. For instance, by declaring an intent filter for an activity, you make it possible for other apps to directly start your activity with a certain kind of intent.

With this intent filter, the InstagramLogin Activity can successfully listen to the Redirect URI from Instagram:

        <activity
            android:name=".main.InstagramLogin"
            android:launchMode="singleTop" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <data android:scheme="customscheme" />
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
            </intent-filter>
        </activity>
        <activity
            android:name=".main.MainActivity"
            android:label="@string/title_activity_main" >
        </activity>


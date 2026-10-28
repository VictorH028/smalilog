-- Preset SSL unpinning para smalilog renef.
-- Solo hooks Java: se traducen a stubs Smali estáticos (sin root).
-- Los hooks nativos (libflutter.so, libssl.so, etc.) no se incluyen aquí.

-- TrustManagers: anular la validación de cadena.
hook("javax/net/ssl/X509TrustManager", "checkServerTrusted",
     "([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V",
     { onEnter = function(args) args.skip = true end }, "X509TrustManager")

hook("com/android/org/conscrypt/Platform", "checkServerTrusted",
     "(Ljavax/net/ssl/X509TrustManager;[Ljava/security/cert/X509Certificate;Ljava/lang/String;Lcom/android/org/conscrypt/AbstractConscryptSocket;)V",
     { onEnter = function(args) args.skip = true end }, "Conscrypt Platform (socket)")

hook("com/android/org/conscrypt/Platform", "checkServerTrusted",
     "(Ljavax/net/ssl/X509TrustManager;[Ljava/security/cert/X509Certificate;Ljava/lang/String;Lcom/android/org/conscrypt/ConscryptEngine;)V",
     { onEnter = function(args) args.skip = true end }, "Conscrypt Platform (engine)")

hook("android/security/net/config/NetworkSecurityTrustManager", "checkServerTrusted",
     "([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V",
     { onEnter = function(args) args.skip = true end }, "NetworkSecurityTrustManager")

hook("android/security/net/config/RootTrustManager", "checkServerTrusted",
     "([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V",
     { onEnter = function(args) args.skip = true end }, "RootTrustManager")

-- OkHttp / OkHostnameVerifier.
hook("okhttp3/CertificatePinner", "check",
     "(Ljava/lang/String;Ljava/util/List;)V",
     { onEnter = function(args) args.skip = true end }, "OkHttp CertificatePinner")

hook("com/squareup/okhttp/internal/tls/OkHostnameVerifier", "verify",
     "(Ljava/lang/String;Ljavax/net/ssl/SSLSession;)Z",
     { onLeave = function(retval) return true end }, "OkHostnameVerifier (SSLSession)")

hook("com/squareup/okhttp/internal/tls/OkHostnameVerifier", "verify",
     "(Ljava/lang/String;Ljava/security/cert/X509Certificate;)Z",
     { onLeave = function(retval) return true end }, "OkHostnameVerifier (X509)")

-- HostnameVerifier genérico y WebView.
hook("javax/net/ssl/HostnameVerifier", "verify",
     "(Ljava/lang/String;Ljavax/net/ssl/SSLSession;)Z",
     { onLeave = function(retval) return true end }, "HostnameVerifier")

hook("android/webkit/WebViewClient", "onReceivedSslError",
     "(Landroid/webkit/WebView;Landroid/webkit/SslErrorHandler;Landroid/net/http/SslError;)V",
     { onEnter = function(args) args.skip = true end }, "WebViewClient SSL error")

-- Fabric / Appmattus / Flutter (lado Java).
hook("io/fabric/sdk/android/services/network/PinningTrustManager", "checkServerTrusted",
     "([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V",
     { onEnter = function(args) args.skip = true end }, "Fabric PinningTrustManager")

hook("com/appmattus/certificatetransparency/internal/verifier/CertificateTransparencyTrustManager", "checkServerTrusted",
     "([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V",
     { onEnter = function(args) args.skip = true end }, "Appmattus TrustManager")

hook("diefferson/http_certificate_pinning/HttpCertificatePinning", "checkConnexion",
     "(Ljava/lang/String;Ljava/util/List;Ljava/util/Map;ILjava/lang/String;)Z",
     { onLeave = function(retval) return true end }, "Flutter HttpCertificatePinning")

hook("com/macif/plugin/sslpinningplugin/SslPinningPlugin", "checkConnexion",
     "(Ljava/lang/String;Ljava/util/List;Ljava/util/Map;ILjava/lang/String;)Z",
     { onLeave = function(retval) return true end }, "Flutter SslPinningPlugin")

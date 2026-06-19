class Constants {
  // =====================================================
  // CONFIGURAÇÃO FIREBASE — ALTERE AQUI
  // Siga o README.md para obter esses valores gratuitamente
  // =====================================================

  // Web API Key — Firebase Console > Configurações do Projeto > Web API Key
  static const FIREBASE_API_KEY = 'AIzaSyBjzyh1DgWZBm0968oZ89MPOiZofA02Gd4';

  // URL do Realtime Database — Firebase Console > Realtime Database > URL
  static const FIREBASE_DB_URL = 'https://shop-app-fl-default-rtdb.firebaseio.com';

  // =====================================================
  // URLs da API — não altere abaixo desta linha
  // =====================================================
  static const USER_FAVORITES_URL = '$FIREBASE_DB_URL/userFavorites';
  static const PRODUCT_BASE_URL = '$FIREBASE_DB_URL/products';
  static const ORDER_BASE_URL = '$FIREBASE_DB_URL/orders';
}

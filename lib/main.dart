//files
import 'package:virtual_store/models/auth.dart';
import 'package:virtual_store/providers/cart.dart';
import 'package:virtual_store/models/order_list.dart';
import 'package:virtual_store/providers/product_list.dart';
import 'package:virtual_store/screens/auth_or_home_screen.dart';
import 'package:virtual_store/screens/cart_screen.dart';
import 'package:virtual_store/screens/orders_screen.dart';
import 'package:virtual_store/screens/product_details_screen.dart';
import 'package:virtual_store/screens/product_form_screen.dart';
import 'package:virtual_store/screens/products_screen.dart';
import 'package:virtual_store/utils/routes/app_routes.dart';
//packages
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'utils/custom_routes.dart';

void main() => runApp(const ShopApp());

class ShopApp extends StatelessWidget {
  const ShopApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => Auth(),
        ),
        ChangeNotifierProxyProvider<Auth, ProductsList>(
          create: (_) => ProductsList(),
          update: (context, auth, previous) {
            return ProductsList(
              auth.token ?? '',
              previous?.items ?? [],
              auth.userId ?? '',
            );
          },
        ),
        ChangeNotifierProxyProvider<Auth, OrderList>(
          create: (_) => OrderList(),
          update: (context, auth, previous) {
            return OrderList(auth.token ?? '', auth.userId ?? '', previous?.items ?? []);
          },
        ),
        ChangeNotifierProvider(
          create: (_) => Cart(),
        ),
      ],
      child: MaterialApp(
        darkTheme: ThemeData.dark(
          useMaterial3: false,
        ),
        themeMode: ThemeMode.system,
        debugShowCheckedModeBanner: false,
        title: 'Bem-Vindo!',
        // home: const ProductsOverViewScreen(),
        theme: ThemeData(
          useMaterial3: false,
          colorScheme: ColorScheme.fromSwatch().copyWith(
            primary: Colors.orange[900],
            secondary: Colors.deepPurpleAccent.shade200,
          ),
          fontFamily: 'Lato',
          pageTransitionsTheme: PageTransitionsTheme(
            builders: {
              //define transicoes diferentes pelo tipo de plataforma
              TargetPlatform.android: CustomPageTransitionBuilder(),
              TargetPlatform.iOS: CustomPageTransitionBuilder(),
            },
          ),
        ),
        routes: {
          AppRoutes.AUTH_OR_HOME: (context) => const AuthOrHomeScreen(),
          AppRoutes.PRODUCT_DETAILS_SCREEN: (context) => const ProductDetailsScreen(),
          AppRoutes.CART: (context) => const CartScreen(),
          AppRoutes.ORDERS: (context) => const OrdersScreen(),
          AppRoutes.PRODUCTS: (context) => const ProductsScreen(),
          AppRoutes.PRODUCT_FORM: (context) => const ProductFormScreen(),
        },
      ),
    );
  }
}

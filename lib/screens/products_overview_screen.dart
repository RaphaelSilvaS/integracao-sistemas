//files
import 'package:virtual_store/providers/cart.dart';
import 'package:virtual_store/providers/product_list.dart';
import 'package:virtual_store/utils/routes/app_routes.dart';
import '../components/badge.dart';
import '../components/main_drawer.dart';
import '../components/product_gridview.dart';
//packages
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

enum FilterOptions {
  Favorite,
  All,
}

class ProductsOverViewScreen extends StatefulWidget {
  const ProductsOverViewScreen({
    super.key,
  });

  @override
  State<ProductsOverViewScreen> createState() => _ProductsOverViewScreenState();
}

class _ProductsOverViewScreenState extends State<ProductsOverViewScreen> {
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();

    Provider.of<ProductsList>(
      context,
      listen: false,
    ).loadProducts().then((value) {
      setState(() {
        _isLoading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<ProductsList>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Produtos'),
        centerTitle: true,
        actions: [
          PopupMenuButton(
            shadowColor: Theme.of(context).colorScheme.secondary,
            icon: const Icon(Icons.more_vert_rounded),
            itemBuilder: (_) => [
              const PopupMenuItem(
                value: FilterOptions.Favorite,
                child: Text('Apenas Favoritos'),
              ),
              const PopupMenuItem(
                value: FilterOptions.All,
                child: Text('Todos os Itens'),
              ),
            ],
            onSelected: (FilterOptions selectValue) {
              if (selectValue == FilterOptions.Favorite) {
                provider.showFavoriteOnly();
              } else {
                provider.showAll();
              }
            },
          ),
          Consumer<Cart>(
            child: IconButton(
              icon: const Icon(Icons.shopping_cart),
              onPressed: () => {
                Navigator.of(context).pushNamed(AppRoutes.CART),
              },
            ),
            builder: (ctx, cart, child) => BadgeWidget(
              value: cart.itemsCount.toString(),
              child: child!,
            ),
          ),
        ],
      ),
      body: _isLoading
          ? Center(
              child: CircularProgressIndicator(),
            )
          : ProductGridView(),
      drawer: const MainDrawer(),
    );
  }
}

//files
import 'package:virtual_store/components/main_drawer.dart';
import 'package:virtual_store/components/order_item.dart';
import 'package:virtual_store/models/order_list.dart';
//packages
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class OrdersScreen extends StatelessWidget {
  const OrdersScreen({super.key});

  Future<void> _refreshProducts(BuildContext context) {
    return Provider.of<OrderList>(
      context,
      listen: false,
    ).loadOrders();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Meus Pedidos'),
      ),
      body: RefreshIndicator(
        onRefresh: () => _refreshProducts(context),
        child: FutureBuilder(
          future: Provider.of<OrderList>(context, listen: false).loadOrders(),
          builder: (ctx, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(child: CircularProgressIndicator());
            } else if (snapshot.error != null) {
              return Center(
                child: Text('Ocorreu um erro! Contate o Administrador do sistema.'),
              );
            } else {
              return Consumer<OrderList>(
                builder: (context, orders, child) => ListView.builder(
                  itemCount: orders.itemsCount,
                  itemBuilder: (context, index) => OrderWidget(
                    order: orders.items[index],
                  ),
                ),
              );
            }
          },
        ),
      ),

      // body: RefreshIndicator(
      //   onRefresh: () => _refreshProducts(context),
      //   child: _isLoading
      //       ? Center(
      //           child: CircularProgressIndicator(),
      //         )
      //       : ListView.builder(
      //           itemCount: orders.itemsCount,
      //           itemBuilder: (context, index) => OrderWidget(
      //             order: orders.items[index],
      //           ),
      //         ),

      drawer: const MainDrawer(),
    );
  }
}

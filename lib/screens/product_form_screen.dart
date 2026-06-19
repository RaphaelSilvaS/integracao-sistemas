import 'package:virtual_store/models/product_model.dart';
import 'package:virtual_store/providers/product_list.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ProductFormScreen extends StatefulWidget {
  const ProductFormScreen({super.key});

  @override
  State<ProductFormScreen> createState() => _ProductFormScreenState();
}

class _ProductFormScreenState extends State<ProductFormScreen> {
  final _priceFocus = FocusNode();
  final _descriptionFocus = FocusNode();
  final _formkey = GlobalKey<FormState>();
  final _formData = <String, Object>{};
  bool _isLoading = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    if (_formData.isEmpty) {
      final arg = ModalRoute.of(context)?.settings.arguments;

      if (arg != null) {
        final product = arg as Product;
        _formData['id'] = product.id;
        _formData['name'] = product.name;
        _formData['price'] = product.price;
        _formData['description'] = product.description;
        _formData['imageUrl'] = product.imageURL;
      }
    }
  }

  @override
  void dispose() {
    _priceFocus.dispose();
    _descriptionFocus.dispose();
    super.dispose();
  }

  Future<void> _submitForm() async {
    final isValid = _formkey.currentState?.validate() ?? false;
    if (!isValid) return;

    _formkey.currentState?.save();
    setState(() => _isLoading = true);

    try {
      await Provider.of<ProductsList>(context, listen: false).saveProduct(_formData);
      Navigator.of(context).pop();
    } catch (error) {
      await showDialog<void>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Ocorreu um erro'),
          content: const Text('Não foi possível salvar o produto.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Ok'),
            )
          ],
        ),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Formulário de Produto'),
        actions: [
          IconButton(
            onPressed: _submitForm,
            icon: const Icon(Icons.save),
          )
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(12),
              child: Form(
                key: _formkey,
                child: ListView(
                  children: [
                    TextFormField(
                      initialValue: _formData['name']?.toString(),
                      decoration: const InputDecoration(labelText: 'Nome'),
                      textInputAction: TextInputAction.next,
                      onFieldSubmitted: (_) {
                        FocusScope.of(context).requestFocus(_priceFocus);
                      },
                      onSaved: (name) => _formData['name'] = name ?? '',
                      validator: (_name) {
                        final name = _name ?? '';
                        if (name.trim().isEmpty) return 'Nome é obrigatório.';
                        if (name.trim().length < 3) return 'Nome precisa de no mínimo 3 letras.';
                        return null;
                      },
                    ),
                    TextFormField(
                      initialValue: _formData['price']?.toString(),
                      decoration: const InputDecoration(labelText: 'Preço (R\$)'),
                      textInputAction: TextInputAction.next,
                      focusNode: _priceFocus,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      onFieldSubmitted: (_) {
                        FocusScope.of(context).requestFocus(_descriptionFocus);
                      },
                      onSaved: (price) => _formData['price'] = double.parse(price ?? '0'),
                      validator: (_price) {
                        final price = double.tryParse(_price ?? '') ?? -1;
                        if (price <= 0) return 'Informe um preço válido.';
                        return null;
                      },
                    ),
                    TextFormField(
                      initialValue: _formData['description']?.toString(),
                      decoration: const InputDecoration(labelText: 'Descrição'),
                      focusNode: _descriptionFocus,
                      keyboardType: TextInputType.multiline,
                      maxLines: 3,
                      onSaved: (description) {
                        _formData['description'] = description ?? '';
                        _formData['imageUrl'] = _formData['imageUrl'] ?? '';
                      },
                      validator: (_description) {
                        final description = _description ?? '';
                        if (description.trim().isEmpty) return 'Descrição é obrigatória.';
                        if (description.trim().length < 10) return 'Descrição precisa de no mínimo 10 letras.';
                        return null;
                      },
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}

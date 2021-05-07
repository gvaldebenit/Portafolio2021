# Generated by Django 3.1.2 on 2021-05-07 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('idCargo', models.AutoField(primary_key=True, serialize=False)),
                ('cargo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('idCiudad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('rut', models.CharField(max_length=10)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidoPaterno', models.CharField(max_length=20)),
                ('apellidoMaterno', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=9)),
                ('direccion', models.CharField(max_length=40)),
                ('idCliente', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('rut', models.CharField(max_length=10)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidoPaterno', models.CharField(max_length=20)),
                ('apellidoMaterno', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=9)),
                ('direccion', models.CharField(max_length=40)),
                ('idEmpleado', models.AutoField(primary_key=True, serialize=False)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.cargo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FamiliaProducto',
            fields=[
                ('idFamiliaProducto', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('idRegion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('idRubro', models.AutoField(primary_key=True, serialize=False)),
                ('rubro', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('idVenta', models.AutoField(primary_key=True, serialize=False)),
                ('fechaVenta', models.DateTimeField()),
                ('total', models.IntegerField()),
                ('estado', models.IntegerField()),
                ('idCliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('idTipoProducto', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=40)),
                ('idFamProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.familiaproducto')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('rut', models.CharField(max_length=10)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidoPaterno', models.CharField(max_length=20)),
                ('apellidoMaterno', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=9)),
                ('direccion', models.CharField(max_length=40)),
                ('idProveedor', models.AutoField(primary_key=True, serialize=False)),
                ('representante', models.CharField(max_length=50)),
                ('idRubro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.rubro')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.CharField(max_length=17, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=200)),
                ('precio', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('stockCrit', models.IntegerField()),
                ('fVenc', models.DateField()),
                ('imagen', models.ImageField(null=True, upload_to='productos')),
                ('idFamProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.familiaproducto')),
                ('idProveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.proveedor')),
                ('idTipoProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.tipoproducto')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('idOrdenCompra', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('total', models.IntegerField()),
                ('comentario', models.CharField(blank=True, max_length=200)),
                ('idEmpleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.empleado')),
                ('idProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('nroFactura', models.AutoField(primary_key=True, serialize=False)),
                ('fechaEmision', models.DateTimeField()),
                ('neto', models.IntegerField()),
                ('iva', models.IntegerField()),
                ('total', models.IntegerField()),
                ('idVenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.venta')),
            ],
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('idDetalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precioUnitario', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('idProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.producto')),
                ('idVenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.venta')),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('idComuna', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('idCiudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.ciudad')),
            ],
        ),
        migrations.AddField(
            model_name='ciudad',
            name='idRegion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.region'),
        ),
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('nroBoleta', models.AutoField(primary_key=True, serialize=False)),
                ('fechaEmision', models.DateTimeField()),
                ('totalBoleta', models.IntegerField()),
                ('idVenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebPage.venta')),
            ],
        ),
    ]

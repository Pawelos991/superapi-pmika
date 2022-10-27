#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

typedef unsigned long long ulong;

// 64 bitowy generator pseudolosowy
//---------------------------------
ulong Losuj ( ulong a, ulong b )
{
  ulong w=0;

  for(int i = 1; i <= 8; i++ )
  {
    w <<= 8;
    w |= rand( ) % 256;
  }
  return ( ( w % ( b - a ) ) + a );
}

// Funkcja mnoży a i b mod n
//--------------------------
ulong MnozModulo ( ulong a, ulong b, ulong n )
{
  ulong m, w;

  w = 0;
  for( m = 1; m; m <<= 1 )
  {
    if( b & m ) w = ( w + a ) % n;
    a = ( a << 1 ) % n;
  }
  return w;
}

// Funkcja oblicza a^e mod n
//--------------------------
ulong PotegujModulo ( ulong a, ulong e, ulong n )
{
  ulong m, p, w;

  p = a;
  w = 1;
  for( m = 1; m; m <<= 1 )
  {
    if( e & m ) w = MnozModulo ( w, p, n );
    p = MnozModulo ( p, p, n );
  }
  return w;
}

bool isPrime(ulong p) {

  ulong a, d, x;
  int s = 0;
  bool t = true;

  srand ( ( unsigned ) time ( NULL ) );
  for( d = p - 1; d % 2 == 0; s++ ) d = d >> 1;
  for(int i = 1; i <= 14; i++ )
  {
    a = Losuj ( 2, p );
    x = PotegujModulo ( a, d, p );
    if( ( x == 1 ) || ( x == p - 1 ) ) 
      continue;
    for(int j = 1; ( j < s ) && ( x != p - 1 ); j++ )
    {
      x = MnozModulo ( x, x, p );
      if( x == 1 )
      {
        t = false; 
        break;
      }
    }
    if( !t ) break;
    if( x != p - 1 )
    {
      t = false; 
      break;
    }
  }
  return t;
}
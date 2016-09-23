#!/usr/bin/perl
#
# CS3700, Northeastern University
# Project 1
#
# This code provides a sample of how one might structure a bridge program.  This example code
# simply connects to the specified LANs and broadcasts "Hello!" messages once every 500ms. 
# It also prints out any messages that it receives on the LANs.  It does *not* actually read or 
# process any of these messages, maintain any forwarding tables, create BPDUs, etc.
#
# You **should not** try to use this as a basis for your code unless you are very comfortable
# with perl.  Instead, use this as a guide for setting up your basic code in your language of
# choice.

use strict;
use warnings;
use IO::Select;
use IO::Socket;
use IO::Socket::UNIX;
use JSON::PP;
use Time::HiRes qw(time sleep);

$| = 1;

# Read in arguments
if ($#ARGV < 1) { 
  die "Usage: ./3700bridge id lan-name [lan-name ...]";
}

# Get my ID
my $id = $ARGV[0];

my $SLEEP_TIMEOUT = 0.5;

# Build my IO Selector
my $sel = IO::Select->new();

# Data structure storing port -> Socket
my @ports = ();
my %portlookup = ();

# Connect ports to LANs
for (my $i=1; $i<=$#ARGV; $i++) {
  # You **must** pad the path with NULLs to get the right socket
  my $SOCK_PATH = "\0$ARGV[$i]"  . ("\0" x 256);

  my $client = IO::Socket::UNIX->new(
     Type => SOCK_SEQPACKET,
     Peer => $SOCK_PATH
  );

  die "Can't create socket for lan '$ARGV[$i]': $!" unless $client;
  $client->autoflush(1);

  $sel->add($client);

  push @ports, $client;
  $portlookup{$client->fileno} = $i-1;
}

print "Bridge $id starting up\n";

my $last_sent = time;

while (1) {
  # Determine how long I can sleep for before the next "Hello" broadcast
  my $sleep = $SLEEP_TIMEOUT - (time - $last_sent);

  # Go to sleep, but wake when any port is readable
  my @ready = $sel->can_read($sleep);

  # When I awake, read any ports that have data
  foreach my $fh (@ready) {
    my $msg = "";
    $fh->recv($msg, 1500);
    if ($msg) {
      # Print out that I received a message
      print "Recv on port " . $portlookup{$fh->fileno} . ": $msg\n";
    } else {
      # Disconnect the port if an error occured
      $sel->remove($fh);
    }
  }

  # If it's time to broadcast, send the message
  if (time - $last_sent > $SLEEP_TIMEOUT) {
    for (my $i=0; $i<=$#ports; $i++) {
      my $sock = $ports[$i];
      print $sock encode_json({"source" => $id, "dest" => "ffff", "type" => "data", "message" => {"data" => "Hello!"}});
    }
    $last_sent = time;
  }
}

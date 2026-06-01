#!/usr/bin/env perl
use strict;
use warnings;
use JSON::PP;
use Getopt::Long;

my $in  = '-';
my $out = 'events.jsonl';
GetOptions('in=s' => \$in, 'out=s' => \$out) or exit 1;

my $fh_in = \*STDIN;
if ($in ne '-') {
    open $fh_in, '<', $in or die "open $in: $!";
}

open my $fh_out, '>', $out or die "open $out: $!";
my $json = JSON::PP->new->canonical(0);

while (my $line = <$fh_in>) {
    chomp $line;
    next if $line !~ /\S/;

    my ($layer, $msg) = ('OTHER', $line);
    if ($line =~ /NAS:\s*(.+)/) {
        $layer = 'NAS';
        $msg   = $1;
    } elsif ($line =~ /AS:\s*(.+)/) {
        $layer = 'AS';
        $msg   = $1;
    } elsif ($line =~ /PM:\s*(.+)/) {
        $layer = 'PM';
        $msg   = $1;
    } elsif ($line =~ /traffic:\s*(.+)/) {
        $layer = 'TRAFFIC';
        $msg   = $1;
    } elsif ($line =~ /idle:\s*(.+)/) {
        $layer = 'IDLE';
        $msg   = $1;
    }

    print $fh_out $json->encode({
        raw   => $line,
        layer => $layer,
        msg   => $msg,
    }) . "\n";
}

close $fh_out;
print STDERR "[normalize_logs] wrote $out\n";

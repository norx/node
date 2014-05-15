### NODE - The (NO)RX (D)ifferential-Search (E)ngine

The research paper associated to this framework is [Report 2014/317](https://eprint.iacr.org/2014/317) of the IACR Cryptology ePrint Archive.

####Usage
Compile [STP](https://stp.github.io/stp/) and copy the binary `stp` to the folder `bin`. To start a search execute
```
./node.py -d {database} -e {entry}
```
where `database` and `entry` can be found in the settings file `config.json`. Moreover, execute
```
./node.py -d {database} -e {entry} -p
```
to display the used CVC code, without doing a search.


####Requirements

  * [STP](https://stp.github.io/stp/)
  * [Boolector](http://fmv.jku.at/boolector/) (optional)
  * [CryptoMiniSat](https://github.com/msoos/cryptominisat) (optional)

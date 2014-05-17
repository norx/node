### NODE - The (NO)RX (D)ifferential-Search (E)ngine

The research paper associated to this framework is [Report 2014/317](https://eprint.iacr.org/2014/317) of the IACR Cryptology ePrint Archive.

####Requirements

  * [STP](https://stp.github.io/stp/)
  * [Boolector](http://fmv.jku.at/boolector/) (optional)
  * [CryptoMiniSat](https://github.com/msoos/cryptominisat) (optional)

NODE searches for `stp` in `node/bin` or in $PATH (in that order). Thus, either install STP globally or copy the binary `stp` to the folder `node/bin`. The same holds for the other two supported solvers `boolector` and `cryptominisat`.

####Usage
To start a differential search execute
```
./node.py -d {database} -e {entry}
```
where `database` and `entry` can be found in the settings file `config.json`. The results of a search are written to the folder `tmp`. Moreover, execute
```
./node.py -d {database} -e {entry} -p
```
to display the generated CVC code, without doing a search.

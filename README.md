### NODE - The (NO)RX (D)ifferential-Search (E)ngine

NODE is a framework to analyse differential propagation in the NORX authenticated encryption scheme. The accompanying research paper can be found on the IACR Cryptology ePrint Archive as [Report 2014/317](https://eprint.iacr.org/2014/317).

####Requirements

  * [STP](https://stp.github.io/stp/)
  * [Boolector](http://fmv.jku.at/boolector/) (optional)
  * [CryptoMiniSat](https://github.com/msoos/cryptominisat) (optional)


####Setup
NODE searches for `stp` in `node/bin` or in $PATH (in that order). Thus, either install STP globally or copy/link the `stp` binary to `node/bin/stp`. The same holds for the other two supported solvers `boolector` and `cryptominisat`.

NODE includes `stp` and `cryptominisat` as submodules. To check them out simply execute
```
git submodule init
git submodule update
```

in the `node` root folder.


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

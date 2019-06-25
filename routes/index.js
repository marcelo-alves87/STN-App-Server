var express = require('express');
var multer = require('multer');
var fs = require('fs');
var router = express.Router();
var path = require("path");
var exec = require("child_process").exec;
const UPLOAD_PATH = '../python/';
var uuid = require('uuid')

var store = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, './python');
    },
    filename: function(req, file, cb) {
        cb(null, file.originalname);
    }
});

router.get('/', function(req,res) {
    res.json('Hello World!');
});

var upload = multer({storage: store}).single('file');

router.post('/fileUpload', function (req, res, next) {
    upload(req, res, function(err) {
        if(err) {
            return res.status(501).json({error:err});
        }

        return res.json({originalname:req.file.originalname, uploadname: req.file.filename})
    });
});


function unlinkSyncFile(fileName) {
    path1 = path.resolve(__dirname, UPLOAD_PATH, fileName);
    if(fs.existsSync(path1)) {
        fs.unlinkSync(path1);
    }
}

function execPython(fileName, res, basename) {
    //STN - MED02mWorkshop - R.04.2019 - RNA.1001.14.1
    //STN - MEDExpUFPEWorkshop - R.03.2019 - RNA.1001.14.1
    exec('python ./python/' + '"' + basename + '.py" ' + '"' + fileName + '"', (error, stdout, stderr) => {
        if (error) {
          console.error('exec error:' + error);
          return;
        }
        res.json({'print' : stdout });            
        setTimeout(unlinkSyncFile, 1000, fileName);
    });
}

function execPython2(fileName, res) {
    exec('python ./python/plot.py ' + '"' + fileName + '"', (error, stdout, stderr) => {
        if (error) {
          console.error('exec error:' + error);
          return;
        }
       
        res.json({'image' : base64_encode(fileName + '.png')});
       
        setTimeout(unlinkSyncFile, 1000, fileName);    
        setTimeout(unlinkSyncFile, 2000, fileName + '.png');
     
      });
}

function processEncodedFile(fileEncoded, res, typeProcess) {
    fileEncoded = fileEncoded.replace('data:application/vnd.ms-excel;base64,', '');
    fileEncoded = fileEncoded.replace('data:text/comma-separated-values;base64,', '');
    fileName = uuid.v4().toString() + '.csv';
    fs.writeFile('python/' + fileName, fileEncoded, 'base64', function(err) {
        if(err) {
            console.log(err);
        } else {
            if(typeProcess == 0) {
                setTimeout(execPython, 1000, fileName, res, 'STN - MED02mWorkshop - R.04.2019 - RNA.1001.14.1');
            } else if (typeProcess == 1) {
                setTimeout(execPython, 1000, fileName, res, 'STN - MEDExpUFPEWorkshop - R.03.2019 - RNA.1001.14.1');
            } else if(typeProcess == 2) {
                setTimeout(execPython2, 1000, fileName, res);
            }
        }
    });
}

// function to encode file data to base64 encoded string
function base64_encode(fileName) {
    path1 = path.resolve(__dirname, UPLOAD_PATH, fileName);
    if(fs.existsSync(path1)) {
        // read binary data
        var bitmap = fs.readFileSync(path1);
        // convert binary data to base64 encoded string
        return Buffer.from(bitmap).toString('base64');
    }    
}

router.post('/fileProcess', function(req,res) {
  processEncodedFile(JSON.stringify(req.body.fileName), res, req.body.typeProcess);
});

module.exports = router;
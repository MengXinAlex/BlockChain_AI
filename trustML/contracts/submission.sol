pragma solidity ^0.4.24;

contract DataSubmission {
  //Structure for each submission
  struct Submission {
    uint8 accuracy;
    uint8 precision;
    uint8 recall;
    uint8 fscore;
    uint16 rank;
    uint8 score;
    uint256[] accset;
    uint256[] uncset;
    bool paid;
  }
  // Mapping for each model to each submission for an address
  mapping(uint8 => mapping (address => Submission)) public model_submissions;
  //Mapping for our models indexes
  mapping(uint8 => address[]) public model_indexes;

  //Mapping for our total submissions per model
  mapping(uint8 => uint16) public model_total;

  // To store the address of the best submission
  address best_submission;
  // To store total number of submission
  uint16 total_submissions = 0;
  uint8[] mapping_id;


  //Constructor
  constructor() public {
  }
  //Creates a Submission from the data and stores it in the Submissions mapping
  function submitData(uint8 _id, address _account, uint8 _accuracy, uint8 _precision, uint8 _recall, uint8 _fscore, uint8 _score, uint256[] _accset,  uint256[] _uncset) public {
       model_indexes[_id].push(_account);
       model_total[_id] = model_total[_id]+1;
       // paid is set to false by default
       Submission memory s = Submission(_accuracy,_precision,_recall, _fscore, total_submissions, _score,  _accset, _uncset, false);
       model_submissions[_id][_account] = s;


  }
  // Setter to set Rank, Not yet complete
  function setRank(address _account) public{
  }
  // Getter to get similarity for an address
  function getAccuracy(uint8 id, address _account) view public returns (uint8){
      return model_submissions[id][_account].accuracy;
  }
  // Getter to get evaluation for an address
  function getPrecision(uint8 id, address _account) view public returns (uint8){
      return model_submissions[id][_account].precision;
  }
  // Getter to get score for an address
  function getRecall(uint8 id, address _account) view public returns (uint8){
      return model_submissions[id][_account].recall;
  }
  // Getter to get score for an address
  function getFscore(uint8 id, address _account) view public returns (uint8){
      return model_submissions[id][_account].fscore;
  }
   // Getter to get accuracy set for an address
  function getAccset(uint8 id, address _account) view public returns (uint256[]){
      return model_submissions[id][_account].accset;
  }
   // Getter to get accuracy set for an address
  function getUncset(uint8 id, address _account) view public returns (uint256[]){
      return model_submissions[id][_account].uncset;
  }

  
  // Getter to get senders Address, this is differen to other address' as they are the ethereum account address
  function senderAddress() view public returns (address){
      return msg.sender;
  }

  function getSubmission(uint8 id, uint16 index) view public returns (uint8,uint8,uint8,uint8,uint8){
      uint8 accuracy = model_submissions[id][model_indexes[id][index]].accuracy;
      uint8 precision = model_submissions[id][model_indexes[id][index]].precision;
      uint8 recall = model_submissions[id][model_indexes[id][index]].recall;
      uint8 fscore = model_submissions[id][model_indexes[id][index]].fscore;
      uint8 score = model_submissions[id][model_indexes[id][index]].score;
      return (accuracy,precision,recall,fscore,score);
  }

  function getSubmissionAU(uint8 id, uint16 index) view public returns (uint256[],uint256[]){
      
      uint256[] accset = model_submissions[id][model_indexes[id][index]].accset;
      uint256[] uncset = model_submissions[id][model_indexes[id][index]].uncset;
      return (accset, uncset);
  }

  function getRank(address _account) view public returns (uint16){
      return 1;
  }

  function getTotalSubmissions(uint8 id) view public returns (uint16){
      return model_total[id];
  }
  function getSubmissionAccount(uint8 id, uint256 index) view public returns (address){
      return model_indexes[id][index];
  }

  // Had to split up because the stack got too deep
  function getPaid(uint8 id, uint16 index) view public returns (bool) {
    return model_submissions[id][model_indexes[id][index]].paid;
  }

  // Call this once the reward has been made
  function setPaid(uint8 id, address _account) public {
    model_submissions[id][_account].paid = true;
  }

}

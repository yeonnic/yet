

// this is comment remove test!!
contract Owned{

  address owner;
  address test;
  uint256 A;
  address B = address(0x1234);
  address C = msg.sender;
  uint256 D = 10e18;
  mapping(address=>uint256) test_balance;

  constructor(){
    owner = msg.sender;
  }

  modifier onlyOwner(){
    require(owner == msg.sender);
    _;
  }

  /*
  function test_owner_01(){
    require( owner == msg.sender );
  }

  modifier test_owner_02(){
    if( owner != msg.sender) throw;
    _;
  }
  */
}

contract test is Owned{

  mapping(address=>uint256) public balance;

  string public a = "This is comment remove test!! https://123123123"; 
  
  event Transfer(address from, address to, uint256 amount);

  constructor(){
    balance[msg.sender] = 10e18;
    
    emit Transfer(address(0), msg.sender, 10e18);
  }

  function transfer(address _to, uint256 amount) public {
    require(balance[msg.sender] >= amount);
    require(_to != address(0));

    balance[msg.sender] -= amount;
    balance[_to] += amount;
    
    emit Transfer(msg.sender, _to, amount);
  }

  function mint(address _to, uint256 amount) onlyOwner public{ //fuck regx
    balance[_to] += amount;

    emit Transfer(address(0), _to, amount);
  }

  function rand(uint256 num) internal returns(uint256){ //test
    return uint256(blockhash(block.number)) % num;
  }


  /* 123 */

  /**
    * asdf
    */

    /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */

  ///123123

  //fuck fuckuck
}
